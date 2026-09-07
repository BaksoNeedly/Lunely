from typing import Any

from lunely.packets.packet import Packet


class TemplatePacket(Packet):
    
    def __init__(
        self,
        type: str,
        data: dict[str, str]
    ) -> None:
        self._type = type.strip().lower()
        self._data = data
        super().__init__()
        
    def to_data(self) -> dict[str, Any]:
        return {
            "type": self._type,
            "data": self._data
        }
        
    @staticmethod
    def from_data(data: dict[str, str]) -> "TemplatePacket":
        packet_type = str(data.get("type"))
        packet_data = data.get("data")
        
        if not isinstance(packet_data, dict):
            raise ValueError("'data' has to be dictionary.")
        return TemplatePacket(packet_type, packet_data)