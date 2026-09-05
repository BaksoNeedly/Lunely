class WebSocketFrame:

    @staticmethod
    def parse(frame: bytes):
        byte2 = frame[1]
        length = byte2 & 0b01111111        

        if length <= 125:
            payload = frame[6:6 + length]
            mask_key = frame[2:6]
        elif length == 126:
            payload = frame[8:8 + int.from_bytes(frame[2:4], "big")]
            mask_key = frame[4:8]
        elif length == 127:
            payload = frame[14:14 + int.from_bytes(frame[2:10], "big")]
            mask_key = frame[10:14]

        numbers = []
        for i, byte in enumerate(payload):
            numbers.append(byte ^ mask_key[i % 4])

        return bytes(numbers)

    @staticmethod
    def build(data: bytes):
        byte1 = 0b10000001
        length = len(data)

        if length <= 125:
            byte2 = length
            return bytes([byte1, byte2]) + data
        elif length <= 65535:
            byte2 = 126
            return bytes([byte1, byte2]) + length.to_bytes(2, "big") + data
        else:
            byte2 = 127
            return bytes([byte1, byte2]) + length.to_bytes(8, "big") + data
