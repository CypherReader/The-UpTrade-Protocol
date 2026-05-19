from pydantic import BaseModel
from typing import Optional, List, Dict

# Google Universal Commerce Protocol (UCP) concepts
class UCPProduct(BaseModel):
    id: str
    title: str
    description: Optional[str] = None
    price: Optional[str] = None
    url: str
    attributes: Dict[str, str] = {}

class UCPOffer(BaseModel):
    offered_items: List[UCPProduct]
    requested_items: List[UCPProduct]
    cash_delta: float = 0.0 # Positive if offering cash, negative if requesting cash

class UCPCart(BaseModel):
    id: str
    items: List[UCPProduct]
