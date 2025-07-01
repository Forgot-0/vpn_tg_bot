from aiogram.fsm.state import State, StatesGroup



class CreateSubscriptionStates(StatesGroup):
    waiting_for_days = State()
    waiting_for_devices = State()
    # waiting_for_region = State()
    waiting_for_protocol = State()


class RenewSubscriptionStates(StatesGroup):
    subscription_id = State()
    renew = State()