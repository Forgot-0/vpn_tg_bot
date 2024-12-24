from aiogram.fsm.state import State, StatesGroup



class SubscriptionState(StatesGroup):
    name: str = State()
    description: str = State()
    duration: int = State()
    price: float = State()
    is_active: bool = State()
    limit_ip: int = State()
    limit_trafic: int = State()

