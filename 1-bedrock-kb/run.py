import boto3
import json

def chat_claude_bedrock_with_kb(messages):
    """
    Chat function using Claude via AWS Bedrock with knowledge base integration
    """
    try:
        bedrock_agent_runtime = boto3.client(
            service_name="bedrock-agent-runtime", region_name="us-east-1"
        )

        conversation_history = "\n".join([f"{msg['role']}: {msg['content']}" for msg in messages])

        response = bedrock_agent_runtime.retrieve_and_generate(
            input={
                "text": messages[-1]['content']
            },
            retrieveAndGenerateConfiguration={
                "type": "KNOWLEDGE_BASE",
                "knowledgeBaseConfiguration": {
                    "knowledgeBaseId": "RNJRXF1MS0",
                    "modelArn": "arn:aws:bedrock:us-east-1::foundation-model/anthropic.claude-3-sonnet-20240229-v1:0",
                    "retrievalConfiguration": {
                        "vectorSearchConfiguration": {
                            "numberOfResults": 3
                        }
                    },
                    "generationConfiguration": {
                        "promptTemplate": {
                            "textPromptTemplate": f"""
                            Human: You are an AI assistant named KnowBot. Your role is to help users by providing relevant information from the knowledge base. Always be polite, concise, and helpful. If you're not sure about something, say so. Here's the conversation so far:

                            {conversation_history}

                            Based on this conversation and the following information from the knowledge base, please provide a helpful response to the last query:

                            $search_results$

                            Assistant:
                            """
                        }
                    }
                }
            }
        )

        assistant_message = response['output']['text']
        messages.append({"role": "assistant", "content": assistant_message})

        # Add citations if available
        citations = response.get('citations', [])
        if citations:
            citation_text = "\n\nSources:\n"
            for citation in citations:
                for reference in citation['retrievedReferences']:
                    citation_text += f"- {reference['location'].get('s3Location', {}).get('uri', 'Unknown source')}\n"
            messages[-1]['content'] += citation_text

        return messages

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        raise

def main():
    messages = [
        {"role": "human", "content": "What are some key features of transformers? Explain with a simple analogy."}
    ]
    
    result = chat_claude_bedrock_with_kb(messages)
    for message in result:
        print(f"{message['role']}: {message['content']}")

if __name__ == "__main__":
    main()
 