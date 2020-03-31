"""design pattern via https://youtu.be/S_ipdVNSFlo?t=2153, modified such that validators are _callable_"""

from abc import ABC, abstractmethod

class Validator(ABC):
    def __set_name__(self, owner, name):
        self.private_name = f"_{name}"

    def __call__(self, *, value):
        self.validate(value)
        return value

    @abstractmethod
    def validate(self, value):
        pass
