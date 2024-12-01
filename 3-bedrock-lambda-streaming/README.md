# Minimal Lambda Streaming Example

Use AWS Bedrock with HTTP Lambda Response Streaming to stream chatbot responses with Claude 3.5 Sonnet.

Built with SAM for faster build and deploy times.

## Links

YouTube Channel: https://www.youtube.com/@shawn.builds
YouTube Video:
Full Blog Post: https://shawnesquivel.com/should-you-stream-chatbot-responses-with-aws-lambda/

# Instructions

1. Install dependencies:

```bash
npm install
```

2. Deploy:

```bash
sam deploy --guided
```

## Once successful you should see an output like this:

## Outputs

| Key               | Description                   | Value                                 |
| ----------------- | ----------------------------- | ------------------------------------- |
| StreamingFunction | Streaming Lambda Function URL | https://URL.lambda-url.REGION.on.aws/ |

3. Set environment:

```bash
export LAMBDA_URL=<function-url-from-outputs>
```

4. Test:

```bash
curl -X POST $LAMBDA_URL \
  -H "Content-Type: application/json" \
  -d '{"message":"Tell me a short story"}'
```

5. Cleanup:

```bash
sam delete
```
