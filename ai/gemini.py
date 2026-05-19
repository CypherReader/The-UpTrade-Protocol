import config
from protocols.ucp import UCPProduct
import json
from google import genai
from google.genai import types

def get_client():
    if not config.GEMINI_API_KEY:
        print("WARNING: GEMINI_API_KEY not set. AI functions will return mock data.")
        return None
    return genai.Client(api_key=config.GEMINI_API_KEY)

# Use the latest recommended model
MODEL_NAME = 'gemini-2.5-flash'

def evaluate_trade(current_item: str, prospect: UCPProduct, target_item: str) -> dict:
    """
    Evaluates if the prospect item is a good trade towards the target item.
    Returns a dictionary with 'worth_trading' (bool) and 'reasoning' (str).
    """
    client = get_client()
    if not client:
        # Mock behavior for testing without API key
        return {
            "worth_trading": True,
            "reasoning": "Mock evaluation: Assuming this is a good trade up."
        }

    prompt = f"""
    You are an expert barterer attempting to complete a sequence of trades, similar to the "One Red Paperclip" story.

    Current Inventory: {current_item}
    Ultimate Goal: {target_item}

    Potential Trade Prospect found online:
    Title: {prospect.title}
    Price Listed: {prospect.price}
    URL: {prospect.url}

    Task:
    Evaluate if trading the '{current_item}' for the '{prospect.title}' is a logical "trade up" that gets us closer in value or liquidity to the ultimate goal ('{target_item}').
    Consider realistic resale values and desirability.

    Respond STRICTLY in the following JSON format:
    {{
        "worth_trading": true/false,
        "reasoning": "Detailed explanation of why this is or isn't a good trade"
    }}
    """

    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json"
            )
        )
        result = json.loads(response.text)
        return result
    except Exception as e:
        print(f"Error evaluating trade with Gemini: {e}")
        return {"worth_trading": False, "reasoning": f"Error during evaluation: {e}"}

def generate_outreach_message(current_item: str, prospect: UCPProduct) -> str:
    """
    Generates a natural, persuasive message to the seller offering a trade.
    """
    client = get_client()
    if not client:
        return f"Hi! Would you be interested in trading your {prospect.title} for my {current_item}? Let me know!"

    prompt = f"""
    You are trying to trade your '{current_item}' for a '{prospect.title}' listed on an online marketplace (listed at {prospect.price}).

    Write a short, friendly, and persuasive direct message to the seller offering this trade.
    Do not mention your ultimate goal or that you are an AI. Sound like a normal, reasonable person.
    Keep it concise.
    """

    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt
        )
        return response.text.strip()
    except Exception as e:
        print(f"Error generating message with Gemini: {e}")
        return f"Hi, would you consider trading your item for my {current_item}?"
