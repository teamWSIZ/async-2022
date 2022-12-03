from dataclasses import dataclass


@dataclass
class User:
    uid: int
    name: str
    address: str