
from abc import ABC
from dataclasses import dataclass

from app.infrastructure.mediator.commands import CommandMediator
from app.infrastructure.mediator.queries import QueryMediator



@dataclass(eq=False)
class BaseMediator(CommandMediator, QueryMediator, ABC):
    ...