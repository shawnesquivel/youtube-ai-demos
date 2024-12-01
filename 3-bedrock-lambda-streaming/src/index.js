const {
  BedrockRuntimeClient,
  InvokeModelWithResponseStreamCommand,
} = require("@aws-sdk/client-bedrock-runtime");

const client = new BedrockRuntimeClient({
  region: process.env.AWS_BEDROCK_REGION,
});

exports.handler = awslambda.streamifyResponse(async (event, responseStream) => {
  const body = JSON.parse(event.body);
  const userMessage = body.message;

  const payload = {
    anthropic_version: "bedrock-2023-05-31",
    max_tokens: 1024,
    messages: [
      {
        role: "user",
        content: userMessage,
      },
    ],
  };

  const command = new InvokeModelWithResponseStreamCommand({
    modelId: process.env.BEDROCK_MODEL_ID,
    contentType: "application/json",
    body: JSON.stringify(payload),
  });

  try {
    const apiResponse = await client.send(command);

    responseStream = awslambda.HttpResponseStream.from(responseStream, {
      statusCode: 200,
      headers: {
        "Content-Type": "text/event-stream",
        "Transfer-Encoding": "chunked",
        Connection: "keep-alive",
        "Cache-Control": "no-cache",
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "POST, OPTIONS",
        "Access-Control-Allow-Headers": "Content-Type",
      },
    });

    for await (const chunk of apiResponse.body) {
      const parsed = JSON.parse(new TextDecoder().decode(chunk.chunk.bytes));
      if (parsed.type === "content_block_delta") {
        responseStream.write(parsed.delta.text);
      }
    }

    responseStream.end();
  } catch (error) {
    console.error("Error:", error);
    responseStream = awslambda.HttpResponseStream.from(responseStream, {
      statusCode: 500,
      headers: {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*",
      },
    });
    responseStream.write(JSON.stringify({ error: error.message }));
    responseStream.end();
    return;
  }
});
