from functools import lru_cache
from punq import Container
from infrastructure.depends.container import _init_container
from infrastructure.mediator.mediator import Mediator




@lru_cache(1)
def init_container() -> Container:
    return _init_container()


@lru_cache(1)
def get_mediator() -> Mediator:
    return _init_container().resolve(Mediator) # type: ignore