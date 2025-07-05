from abc import ABC, abstractmethod
from typing import List


class DataBaseInterface(ABC):

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def disconnect(self):
        pass

    @abstractmethod
    def is_collection_existed(self, collection_name: str) -> bool:
        pass

    @abstractmethod
    def list_all_collections(self) -> List[str]:
        pass

    @abstractmethod
    def get_collection_info(self, collection_name: str) -> dict:
        pass

    @abstractmethod
    def delete_collection(self, collection_name: str):
        pass

    @abstractmethod
    def create_collection(self, collection_name: str, do_reset: bool = False):
        pass

    @abstractmethod
    def insert_one(self, collection_name: str, text: str, metadata: dict = None):
        pass

    @abstractmethod
    def insert_many(self, collection_name: str, texts: list, metadata: list = None):
        pass
