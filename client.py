import requests
import uuid
import json

URL = "http://localhost:9000/"


def send_message(user_input):
    payload = {
        "jsonrpc": "2.0",
        "id": str(uuid.uuid4()),
        "method": "message/send",   # IMPORTANT: A2A RPC method
        "params": {
            "message": {
                "role": "user",
                "parts": [
                    {
                        "kind": "text",
                        "text": user_input
                    }
                ],
                "messageId": str(uuid.uuid4())
            },
            "metadata": {}
        }
    }

    response = requests.post(URL, json=payload)
    data = response.json()
    try:
        text = data["result"]["artifacts"][0]["parts"][0]["text"]
        print("\nAgent:", text)
    except (KeyError, IndexError):
        print("RESPONSE:", json.dumps(data, indent=2))


if __name__ == "__main__":
    while True:
        user_input = input("\nYou: ").strip()
        if not user_input:
            continue
        if user_input.lower() in ("exit", "quit"):
            print("Goodbye!")
            break
        send_message(user_input)