from pydantic import BaseModel
from typing import Optional, List
import datetime
import json
import hashlib

# Agent Payments Protocol 2 (AP2) concepts
# Based on documentation regarding Intent Mandates and Cart Mandates for secure agent transactions

class Mandate(BaseModel):
    id: str
    timestamp: str
    agent_id: str
    user_id: str
    type: str # 'intent' or 'cart'

    def sign(self, secret_key: str = "local_dev_key"):
        # In a real implementation, this would use Verifiable Credentials (VCs) and cryptographic signatures
        payload = self.model_dump_json()
        return hashlib.sha256(f"{payload}{secret_key}".encode()).hexdigest()

class IntentMandate(Mandate):
    """
    Specifies the rules of engagement (price limits, timing, conditions).
    Verifiable, pre-authorized proof from the user.
    """
    type: str = "intent"
    target_item: str
    current_inventory: List[str]
    max_cash_addition: float = 0.0
    conditions: str

class CartMandate(Mandate):
    """
    Created once conditions are met. Secure, unchangeable record of exact items.
    Links the Intent Mandate to the specific execution.
    """
    type: str = "cart"
    intent_mandate_id: str
    agreed_offer: str
    counterparty_id: str

def create_barter_intent(inventory_name: str, target_name: str) -> IntentMandate:
    now = datetime.datetime.now(datetime.timezone.utc)
    return IntentMandate(
        id=f"intent_{now.timestamp()}",
        timestamp=now.isoformat(),
        agent_id="trading_agent_1",
        user_id="davidekins@gmail.com",
        target_item=target_name,
        current_inventory=[inventory_name],
        conditions="Trade current inventory for an item of higher value, moving towards the target item. Zero cash addition."
    )
