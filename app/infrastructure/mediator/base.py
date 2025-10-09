
from abc import ABC
from dataclasses import dataclass

from infrastructure.mediator.commands import CommandMediator
from infrastructure.mediator.queries import QueryMediator



@dataclass(eq=False)
class BaseMediator(CommandMediator, QueryMediator, ABC):
    ...