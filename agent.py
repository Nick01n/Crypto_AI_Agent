import os
from smolagents import ToolCallingAgent
from smolagents.models import HuggingFaceModel
from tools import (
    crypto_price,
    crypto_info,
    compare_crypto,
    crypto_history,
    crypto_risk,
)

# 1. Cheking token
HF_TOKEN = os.environ.get("HF_TOKEN")
if not HF_TOKEN:
    raise ValueError("HF_TOKEN not found. Set an environment variable..")

# 2. Hugging Face's model
model = HuggingFaceModel(
    model_id="HuggingFaceH4/zephyr-7b-beta",
    token=HF_TOKEN,
)

# 3. tools
tools = [
    crypto_price,
    crypto_info,
    compare_crypto,
    crypto_history,
    crypto_risk,
]

# 4. Agent
agent = ToolCallingAgent(
    model=model,
    tools=tools,
)

print("Crypto AI Agent is running (type 'exit' to quit)")

while True:
    user_input = input(">> ")
    if user_input.lower() in ("exit", "quit"):
        break

    result = agent.run(user_input)
    print(result)
