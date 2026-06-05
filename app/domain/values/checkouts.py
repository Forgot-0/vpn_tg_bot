from enum import StrEnum


class CheckoutIntent(StrEnum):
    NEW_SUBSCRIPTION = "new_subscription"
    RENEWAL = "renewal"
