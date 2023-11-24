from datetime import datetime


class TimeUtils:
    @staticmethod
    def to_timestamp(datetime_str: str) -> int:
        """Converts a datetime string to a timestamp."""
        dt = datetime.fromisoformat(datetime_str)
        return int(dt.timestamp())

    @staticmethod
    def from_timestamp(timestamp: int) -> str:
        """Converts a timestamp back to a datetime string."""
        dt = datetime.fromtimestamp(timestamp)
        return dt.isoformat()
