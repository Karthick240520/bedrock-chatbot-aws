# Bedrock Chatbot on AWS

A serverless AI chatbot built with Amazon Bedrock (Amazon Nova 2 Lite). The chat page is hosted on S3 and served through CloudFront. Replies come from a Lambda function behind an API Gateway HTTP API.

## Architecture

```
Browser
  -> CloudFront (HTTPS)
  -> S3 (private bucket, index.html)

Browser (chat message)
  -> API Gateway HTTP API  POST /chat
  -> Lambda (Python 3.12)
  -> Amazon Bedrock (Converse API, Nova 2 Lite)
```

## AWS services used

| Service | Purpose |
| --- | --- |
| Amazon Bedrock | Nova 2 Lite model for replies |
| AWS Lambda | Calls the Bedrock Converse API |
| Amazon API Gateway | Public HTTPS endpoint (`POST /chat`) with CORS |
| Amazon S3 | Private bucket storing the chat page |
| Amazon CloudFront | Serves the page over HTTPS (Origin Access Control) |
| AWS IAM | Lets Lambda call Bedrock |

## Files

| File | Description |
| --- | --- |
| `index.html` | Chat page (history, markdown rendering, light and dark mode, mobile friendly) |
| `lambda_function.py` | Lambda backend |
| `README.md` | This file |

## Setup summary

1. **Bedrock:** open the Nova 2 Lite page in the model catalog and test it in the playground (region `us-east-1`).
2. **Lambda:** create `bedrock-chat` (Python 3.12), paste `lambda_function.py`, deploy, set the timeout to 30 seconds.
3. **IAM:** attach an inline policy to the Lambda role allowing `bedrock:InvokeModel` and `bedrock:InvokeModelWithResponseStream`.
4. **API Gateway:** create an HTTP API with a Lambda integration and the route `POST /chat`. Keep the `$default` stage with auto-deploy.
5. **CORS:** allow origin `*`, header `content-type`, methods `POST` and `OPTIONS`.
6. **Page:** set `API_URL` in `index.html` to your endpoint (`https://<api-id>.execute-api.us-east-1.amazonaws.com/chat`).
7. **S3:** create a private bucket (Block all public access ON) and upload `index.html`.
8. **CloudFront:** create a distribution with the bucket as origin, use Origin Access Control, and set the default root object to `index.html`.
9. Open the CloudFront domain name and send a message.

## Test the API from a terminal

```bash
curl -X POST https://<api-id>.execute-api.us-east-1.amazonaws.com/chat \
  -H "Content-Type: application/json" \
  -d '{"messages":[{"role":"user","content":[{"text":"What is AWS?"}]}]}'
```

## Troubleshooting

| Symptom | Fix |
| --- | --- |
| `Internal Server Error` | Increase the Lambda timeout to 30 seconds and check the CloudWatch logs |
| `AccessDeniedException` | Attach the Bedrock inline policy to the Lambda role |
| Replies cut off | Increase `maxTokens` in `lambda_function.py` |
| Page says it could not reach the API | Check CORS settings and the `API_URL` in `index.html` |
| `Access Denied` on the CloudFront URL | Check the bucket policy and that `index.html` is uploaded |
| Old page after an update | Create a CloudFront invalidation for `/*` |

## Security and cost notes

- The API has no login. Add throttling on the API Gateway stage and an AWS Budgets alert.
- Keep the S3 bucket private. Only CloudFront should read it.
- Narrow the Lambda IAM policy to the specific model ARN for production use.
- No API keys or secrets are stored in this repository.

## Possible next steps

- Add Bedrock Knowledge Bases so the bot answers from your own documents.
- Add Bedrock Guardrails for safety filtering.
- Add user authentication (for example Amazon Cognito).
- Define the infrastructure with Terraform.
