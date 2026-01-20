from huggingface_hub import InferenceClient
import os

HF_TOKEN = os.getenv("HF_API_TOKEN")

if not HF_TOKEN:
    raise RuntimeError("HF_API_KEY is missing. Set it as an environment variable.")


client = InferenceClient(
    model="meta-llama/Llama-3.1-8B-Instruct",
    token=HF_TOKEN
)

def generate_response(prompt, max_tokens=900):
    messages = [{
        "role": "user",
        "content": prompt + """
        
Please follow these rules strictly:
- Complete all sections fully.
- Do NOT stop mid-sentence.
- End the response with the word: END
"""
    }]

    response = client.chat_completion(
        messages=messages,
        max_tokens=max_tokens,
        temperature=0.7
    )

    return response.choices[0].message["content"]
