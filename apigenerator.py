import uuid

def generate_api_key():
    return str(uuid.uuid4())

if __name__ == "__main__":
    api_key = generate_api_key()
    print(f"Generated API Key: {api_key}")