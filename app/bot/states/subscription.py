from aiogram.fsm.state import State, StatesGroup


class CreateSubscriptionStates(StatesGroup):
    waiting_for_days = State()
    waiting_for_devices = State()
    # waiting_for_region = State()
    waiting_for_protocol = State()

class SubscriptionStates(StatesGroup):
    subscription_id = State()
    action = State()