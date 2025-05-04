from abc import ABC, abstractmethod
from typing import Any

from domain.entities.server import Server
from domain.entities.subscription import Subscription
from domain.entities.user import User



class BaseApiClient(ABC):
    @abstractmethod
    def create_subscription(self,user: User, subscription: Subscription, server: Server) -> None: ...

    @abstractmethod
    def delete_inactive_clients(self) -> None: ...

    @abstractmethod
    def upgrade_client(self, user: User, subscription: Subscription, server: Server) -> None:...


class BaseProtocolBuilder(ABC):
    @abstractmethod
    def build_params(self, user: User, subscription: Subscription, server: Server) -> dict[str, Any]: ...
