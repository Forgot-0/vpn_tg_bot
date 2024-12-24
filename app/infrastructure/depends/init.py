from functools import lru_cache
from punq import Container
from application.mediator.mediator import Mediator
from infrastructure.depends.container import _init_container




@lru_cache(1)
def init_container() -> Container:
    return _init_container()


@lru_cache(1)
def get_mediator() -> Mediator:
    return _init_container().resolve(Mediator)
