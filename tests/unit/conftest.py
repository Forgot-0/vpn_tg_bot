from uuid import uuid4
import pytest

from domain.entities.server import ProtocolConfig, Server
from domain.entities.subscription import Subscription
from domain.entities.user import User
from domain.services.subscription import SubscriptionPricingService
from domain.values.servers import ApiType, ProtocolType, Region
from infrastructure.api_client.factory import ApiClientFactory
from infrastructure.builders_params.factory import ProtocolBuilderFactory

from tests.mocks.mock_mediator import MockMediator
from tests.mocks.mock_subscription_repository import MockSubscriptionRepository
from tests.mocks.mock_tgbot import MockTelegramBot
from tests.mocks.mock_user_repository import MockUserRepository
from tests.mocks.mock_payment_repository import MockPaymentRepository
from tests.mocks.mock_server_repository import MockServerRepository
from tests.mocks.mock_reward_repository import MockRewardRepository
from tests.mocks.mock_reward_user_repository import MockRewardUserRepository
from tests.mocks.mock_discount_repository import MockDiscountRepository
from tests.mocks.mock_discount_user_repository import MockDiscountUserRepository
from tests.mocks.mock_api_client import MockApiClient
from tests.mocks.mock_protocol_builder import MockProtocolBuilder
from tests.mocks.mock_payment_service import MockPaymentService


@pytest.fixture
def mock_subscription_repository():
    return MockSubscriptionRepository()


@pytest.fixture
def mock_user_repository():
    return MockUserRepository()


@pytest.fixture
def mock_payment_repository():
    return MockPaymentRepository()


@pytest.fixture
def mock_server_repository():
    return MockServerRepository()


@pytest.fixture
def mock_reward_repository():
    return MockRewardRepository()


@pytest.fixture
def mock_reward_user_repository():
    return MockRewardUserRepository()


@pytest.fixture
def mock_discount_repository():
    return MockDiscountRepository()


@pytest.fixture
def mock_discount_user_repository():
    return MockDiscountUserRepository()


@pytest.fixture
def mock_payment_service():
    return MockPaymentService()

@pytest.fixture
def subs_price_service():
    return SubscriptionPricingService(
            daily_rate=2,
            device_rate_multiplier=0.5,
            region_multipliers={
                Region("🇳🇱", "Нидерланды", "NL"): 1.0,
                Region(flag="🇩🇪", name="Germany", code="DE"): 1.0,
            },
            protocol_multipliers={
                ProtocolType.vless: 0.15,
                ProtocolType.mock: 0.15
            }
        )

@pytest.fixture
def dummy_user() -> User:
    return User(telegram_id=123456)

@pytest.fixture
def dummy_subscription(dummy_server, dummy_user) -> Subscription:
    return Subscription(
        user_id=dummy_user.id,
        duration=30,
        server_id=dummy_server.id,
        device_count=1,
        region=Region(flag="🇩🇪", name="Germany", code="DE"),
        protocol_types=[ProtocolType.mock]
    )

@pytest.fixture
def dummy_server() -> Server:
    dummy_protocol_config = ProtocolConfig(
         config={"inbound_id": "inb_123"},
         protocol_type=ProtocolType.mock
    )
    return Server(
        id=uuid4(),
        limit=10,
        free=1,
        region=Region(flag="🇩🇪", name="Germany", code="DE"),
        api_type=ApiType.mock,
        api_config={
            "dummy_data": "mock"
        },
        auth_credits={},
        protocol_configs={ProtocolType.mock: dummy_protocol_config}
    )


@pytest.fixture
def mock_api_client():
    return MockApiClient()


@pytest.fixture
def mock_protocol_builder():
    return MockProtocolBuilder(ProtocolType.mock)


@pytest.fixture
def api_client_factory(mock_api_client):
    factory = ApiClientFactory()
    dummy_api_type = ApiType.mock
    factory.register(dummy_api_type, mock_api_client)
    return factory


@pytest.fixture
def protocol_builder_factory(mock_protocol_builder):
    factory = ProtocolBuilderFactory()
    dummy_api_type = ApiType.mock
    dummy_protocol_type = ProtocolType.mock
    factory.register(dummy_api_type, dummy_protocol_type, type(mock_protocol_builder))
    return factory


@pytest.fixture
def mock_telegram_bot():
    return MockTelegramBot()


@pytest.fixture
def mock_event_mediator():
    return MockMediator()