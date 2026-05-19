from abc import ABC, abstractmethod
from typing import List
from protocols.ucp import UCPProduct

class BasePlatform(ABC):
    @abstractmethod
    def search_items(self, query: str, limit: int = 5) -> List[UCPProduct]:
        """Search the platform and return standardized UCP Products."""
        pass

    @abstractmethod
    def send_message(self, product_url: str, message_content: str, dry_run: bool = True) -> bool:
        """Send a message to the seller of the product."""
        pass
