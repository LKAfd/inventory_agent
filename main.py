import os
import google.generativeai as genai
from dotenv import load_dotenv
from tools import add_items, delete_items, update_items

# Load env
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Choose Gemini model
model = genai.GenerativeModel("gemini-1.5-flash")

def inventory_agent(user_input: str) -> str:
    """Process user input with Gemini and map to tools."""
    prompt = f"""
    You are an Inventory Management Assistant.
    User request: "{user_input}"

    Decide which tool to call:
    - add_items(item_name, quantity)
    - delete_items(item_name)
    - update_items(item_name, quantity)

    Respond with ONLY a valid JSON object, nothing else. Example:
    {{"tool": "add_items", "item_name": "Apples", "quantity": 10}}
    """

    response = model.generate_content(prompt)

    import re, json

    # Extract JSON from response text using regex
    match = re.search(r"\{.*\}", response.text, re.DOTALL)
    if not match:
        return "⚠️ Sorry, I couldn’t parse the request."

    try:
        tool_call = json.loads(match.group())
    except json.JSONDecodeError:
        return "⚠️ Invalid JSON received."

    tool = tool_call.get("tool")
    item = tool_call.get("item_name")
    qty = tool_call.get("quantity")

    if tool == "add_items":
        return add_items(item, qty)
    elif tool == "delete_items":
        return delete_items(item)
    elif tool == "update_items":
        return update_items(item, qty)
    else:
        return "⚠️ Unknown tool requested."

if __name__ == "__main__":
    print("🤖 Inventory Agent is running... Type 'exit' to quit.\n")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            print("👋 Goodbye!")
            break
        result = inventory_agent(user_input)
        print("Agent:", result)