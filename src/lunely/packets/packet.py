from __future__ import annotations

from abc import ABC, abstractmethod

class Packet:

    @abstractmethod
    def get_type(self) -> str:
        return self._type

    @abstractmethod
    def to_data(self) -> dict: pass

    @staticmethod
    @abstractmethod
    def from_data(data) -> Packet: pass
