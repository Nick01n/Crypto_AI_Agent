import os

token = os.environ.get("HF_TOKEN")
if token:
    print("Token is find ✅")
    print(token)
else:
    print("Token is not find ❌")
