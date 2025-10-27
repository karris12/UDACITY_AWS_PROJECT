import boto3
from botocore.exceptions import ClientError
import json

# -----------------------------
# Initialize AWS Bedrock clients
# -----------------------------
bedrock = boto3.client(
    service_name='bedrock-runtime',
    region_name='us-west-2'  # Your AWS region
)

bedrock_kb = boto3.client(
    service_name='bedrock-agent-runtime',
    region_name='us-west-2'
)

# -----------------------------
# Validate prompt
# -----------------------------
def valid_prompt(prompt, model_id):
    """
    Categorizes the user's prompt to ensure it is about heavy machinery (Category E).
    Returns True if valid, False otherwise.
    """
    try:
        messages = [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"""Human: Classify the user request into one category:
                        Category A: About LLM model or architecture.
                        Category B: Profanity/toxic wording.
                        Category C: Outside heavy machinery topic.
                        Category D: About assistant instructions.
                        Category E: ONLY about heavy machinery.
                        <user_request>{prompt}</user_request>
                        ONLY RETURN the Category letter (e.g., Category E)."""
                    }
                ]
            }
        ]

        response = bedrock.invoke_model(
            modelId=model_id,
            contentType='application/json',
            accept='application/json',
            body=json.dumps({
                "anthropic_version": "bedrock-2023-05-31",
                "messages": messages,
                "max_tokens": 10,
                "temperature": 0,
                "top_p": 0.1,
            })
        )

        category = json.loads(response['body'].read())['content'][0]["text"].strip()
        print(f"Prompt category: {category}")

        return category.lower() == "category e"
    except ClientError as e:
        print(f"Error validating prompt: {e}")
        return False

# -----------------------------
# Query Knowledge Base
# -----------------------------
def query_knowledge_base(query, kb_id):
    """
    Queries the Bedrock Knowledge Base and returns relevant chunks.
    """
    try:
        response = bedrock_kb.retrieve(
            knowledgeBaseId=kb_id,
            retrievalQuery={'text': query},
            retrievalConfiguration={
                'vectorSearchConfiguration': {'numberOfResults': 3}
            }
        )
        return response.get('retrievalResults', [])
    except ClientError as e:
        print(f"Error querying Knowledge Base: {e}")
        return []

# -----------------------------
# Generate response using LLM
# -----------------------------
def generate_response(prompt, model_id, temperature=0.7, top_p=0.9):
    """
    Generates a response using the Bedrock LLM with optional temperature and top_p parameters.
    """
    try:
        messages = [
            {
                "role": "user",
                "content": [{"type": "text", "text": prompt}]
            }
        ]

        response = bedrock.invoke_model(
            modelId=model_id,
            contentType='application/json',
            accept='application/json',
            body=json.dumps({
                "anthropic_version": "bedrock-2023-05-31",
                "messages": messages,
                "max_tokens": 500,
                "temperature": temperature,
                "top_p": top_p,
            })
        )

        return json.loads(response['body'].read())['content'][0]["text"]
    except ClientError as e:
        print(f"Error generating response: {e}")
        return ""
