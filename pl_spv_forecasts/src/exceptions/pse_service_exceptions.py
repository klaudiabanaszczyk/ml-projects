from dataclasses import dataclass

@dataclass
class StatusCodeNot200(Exception):
    """
    Custom exception for handling non-200 HTTP status codes.
    """

    status_code: int
    reason: str

    def __str__(self):
        return f"The request failed. Status code: {self.status_code}, reason: {self.reason}."