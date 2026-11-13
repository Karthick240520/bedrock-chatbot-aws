import json
import boto3

client = boto3.client("bedrock-runtime", region_name="us-east-1")
MODEL_ID = "us.amazon.nova-2-lite-v1:0"  # if it errors, try amazon.nova-2-lite-v1:0


def lambda_handler(event, context):
    body = json.loads(event.get("body") or "{}")
    messages = body.get("messages", [])

    resp = client.converse(
        modelId=MODEL_ID,
        system=[{"text": "You are a helpful assistant."}],
        messages=messages,
        inferenceConfig={"maxTokens": 1500, "temperature": 0.5},
    )

    # Nova 2 Lite returns a reasoning block first, so keep only the text parts
    content = resp["output"]["message"]["content"]
    reply = "".join(b["text"] for b in content if "text" in b)

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({"reply": reply}),
    }
