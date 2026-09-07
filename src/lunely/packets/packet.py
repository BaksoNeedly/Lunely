from __future__ import annotations

from abc import abstractmethod

class Packet:
    
    @classmethod
    def get_type(cls) -> str:
        ...

    @abstractmethod
    def to_data(self) -> dict[str, str]:
        ...

    @staticmethod
    @abstractmethod
    def from_data(data: dict[str, str]) -> Packet:
        ...