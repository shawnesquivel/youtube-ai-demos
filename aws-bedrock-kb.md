welcome! in this video, we'll be building a simple knowledge base chatbot using AWS Bedrock.

the special thing about this vidoe, is that we'll set up an AWS OpenSearch Vector database, and use it as our knowledge base.

if you're familiar with vector databases, you'll know that they're optimized for semantic search, which allows us to search for similar documents based on the query.

in practice, I typically use Pinecone or Supabase PGVector for this, but for this video, we'll go use AWS web services fully.

if you like AWS videos like this, make sure to chekc out my "Beginners Generative AI Course" in the description, where we'll build 2 full stack AI applications using NextJS, Python and AWS.

# Pre-requisites

- You should have created an AWS account already.
- You should have created an S3 bucket that you have access to. Make it public for easiest use.

# App Architecture

1. First we'll load some PDFs into an S3 bucket.
2. Next, we'll use AWS Lambda to trigger a function that will read the PDFs, extract the text, and store it in an OpenSearch Vector database.
3. Then, we'll use AWS Bedrock to create a chatbot that will use the OpenSearch Vector database as our knowledge base.

# Step 1: Load PDFs into S3

- Create an S3 bucket
- Upload your PDFs
- Setup public access

# Step 2: Setup AWS Bedrock Models

- Get model access
- Hint: Use us-west-2 as your region to get the latest Claude-3.5-Sonnet models.

# Step 3: Setup the Knowledge Base

- We'll use the quickstart feature to automatically setup the OpenSearch Vector database.
- Disclaimer, because we use the quickstart feature for this devleopment enivronment, we won't be able to automatically deploy this to production.

# Step 4: Setup the RAG Chatbot

- For the RAG chatbot, we'll use a simple NextJS app.
- This chatbot will be pretty barebones, with just a collection of chat histories
- We'll also use AWS Chalice to quickly deploy the API endpoints without too much configuration, but you can use any other framework that you like. I typically use FastAPI.
