from datetime import datetime
import time

# now_ms = int(time.time() * 1000)
# readable_date = datetime.fromtimestamp(now_ms / 1000)

class TimeUtils:

    @staticmethod
    def get_current_time_stamp() -> int:
        return int(time.time() * 1000)
    
    @staticmethod
    def get_timestamp_after_minutes(minutes: int) -> int:
        return (
            TimeUtils.get_current_time_stamp() + (minutes * 60 * 1000)
        )

    @staticmethod
    def convert(stamp: int):
        readable_date = datetime.fromtimestamp(stamp)
        return readable_date