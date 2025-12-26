from dishka import Provider, Scope, provide

from app.application.commands.auth.login import LoginTelegramUserCommand, LoginTelegramUserCommandHandler
from app.application.commands.auth.refresh import RefreshTokenCommand, RefreshTokenCommandHandler
from app.application.commands.payment.paid import PaidPaymentCommand, PaidPaymentCommandHandler
from app.application.commands.servers.create import CreateServerCommand, CreateServerCommandHandler
from app.application.commands.servers.delete import DeleteServerCommand, DeleteServerCommandHandler
from app.application.commands.subscriptions.create import CreateSubscriptionCommand, CreateSubscriptionCommandHandler
from app.application.commands.subscriptions.renew import RenewSubscriptionCommand, RenewSubscriptionCommandHandler
from app.application.commands.users.create import CreateUserCommand, CreateUserCommandHandler
from app.application.events.server.decrement_free import DecrementFreeServerEventHandler
from app.application.queries.servers.get_list import GetListServerQuery, GetListServerQueryHandler
from app.application.queries.servers.get_protocols import GetListProtocolsQuery, GetListProtocolsQueryHandler
from app.application.queries.subscription.get_by_id import GetByIdQuery, GetByIdQueryHandler
from app.application.queries.subscription.get_by_user import GetSubscriptionsUserQuery, GetSubscriptionsUserQueryHandler
from app.application.queries.subscription.get_config import GetConfigQuery, GetConfigQueryHandler
from app.application.queries.subscription.get_list import GetListSubscriptionsQuery, GetListSubscriptionsQueryHandler
from app.application.queries.subscription.get_price import GetPriceSubscriptionQuery, GetPriceSubscriptionQueryHandler
from app.application.queries.tokens.verify import VerifyTokenQuery, VerifyTokenQueryHandler
from app.application.queries.users.get_by_tg_id import GetUserByTgIdQuery, GetUserByTgIdQueryHandler
from app.application.queries.users.get_list import GetListUserQuery, GetListUserQueryHandler
from app.application.queries.users.get_me import GetMeUserQuery, GetMeUserQueryHandler
from app.domain.events.base import BaseEvent
from app.domain.events.paymens.paid import PaidPaymentEvent
from app.infrastructure.log.event_handler import LogHandlerEvent
from app.infrastructure.mediator.commands import CommandRegisty
from app.infrastructure.mediator.event import EventRegisty
from app.infrastructure.mediator.queries import QueryRegistry


class MediatorProvider(Provider):

    log_handler = provide(LogHandlerEvent, scope=Scope.APP)

    create_user_handler = provide(CreateUserCommandHandler, scope=Scope.APP)
    get_user_list_handler = provide(GetListUserQueryHandler, scope=Scope.APP)
    get_me_user_handler = provide(GetMeUserQueryHandler, scope=Scope.APP)

    paid_payment_handler = provide(PaidPaymentCommandHandler, scope=Scope.APP)
    create_subscription_handler = provide(CreateSubscriptionCommandHandler, scope=Scope.APP)
    renew_subscription_handler = provide(RenewSubscriptionCommandHandler, scope=Scope.APP)
    get_list_subscription_handler= provide(GetListSubscriptionsQueryHandler, scope=Scope.APP)
    get_price_subs_handler = provide(GetPriceSubscriptionQueryHandler, scope=Scope.APP)

    tg_id_handler = provide(GetSubscriptionsUserQueryHandler, scope=Scope.APP)
    user_id_handler = provide(GetByIdQueryHandler, scope=Scope.APP)
    config_handler = provide(GetConfigQueryHandler, scope=Scope.APP)

    decrement_server_handler = provide(DecrementFreeServerEventHandler, scope=Scope.APP)
    create_server_handler = provide(CreateServerCommandHandler, scope=Scope.APP)
    delete_server_handler = provide(DeleteServerCommandHandler, scope=Scope.APP)
    get_list_server_handler = provide(GetListServerQueryHandler, scope=Scope.APP)
    get_list_protocols = provide(GetListProtocolsQueryHandler, scope=Scope.APP)

    login_telegram_handler = provide(LoginTelegramUserCommandHandler, scope=Scope.APP)
    refresh_token_handler = provide(RefreshTokenCommandHandler, scope=Scope.APP)
    verify_token_handler = provide(VerifyTokenQueryHandler, scope=Scope.APP)
    get_user_by_tg_id_handler = provide(GetUserByTgIdQueryHandler, scope=Scope.APP)

    @provide(scope=Scope.APP)
    def command_maps(self) -> CommandRegisty:
        command_maps = CommandRegisty()
        command_maps.register_command(
            CreateUserCommand, [CreateUserCommandHandler]
        )

        command_maps.register_command(
            PaidPaymentCommand, [PaidPaymentCommandHandler]
        )

        command_maps.register_command(
            CreateSubscriptionCommand, [CreateSubscriptionCommandHandler]
        )

        command_maps.register_command(
            RenewSubscriptionCommand, [RenewSubscriptionCommandHandler]
        )

        command_maps.register_command(
            CreateServerCommand, [CreateServerCommandHandler]
        )
        command_maps.register_command(
            DeleteServerCommand, [DeleteServerCommandHandler]
        )

        command_maps.register_command(
            LoginTelegramUserCommand, [LoginTelegramUserCommandHandler]
        )
        command_maps.register_command(
            RefreshTokenCommand, [RefreshTokenCommandHandler]
        )
        return command_maps

    @provide(scope=Scope.APP)
    def query_maps(self) -> QueryRegistry:
        query_maps = QueryRegistry()

        query_maps.register_query(
            GetSubscriptionsUserQuery, GetSubscriptionsUserQueryHandler
        )

        query_maps.register_query(
            GetByIdQuery, GetByIdQueryHandler
        )

        query_maps.register_query(
            GetConfigQuery, GetConfigQueryHandler
        )

        query_maps.register_query(
            VerifyTokenQuery, VerifyTokenQueryHandler
        )
        query_maps.register_query(
            GetUserByTgIdQuery, GetUserByTgIdQueryHandler
        )

        query_maps.register_query(
            GetListUserQuery, GetListUserQueryHandler
        )
        query_maps.register_query(
            GetMeUserQuery, GetMeUserQueryHandler
        )
        query_maps.register_query(
            GetListSubscriptionsQuery, GetListSubscriptionsQueryHandler
        )
        query_maps.register_query(
            GetPriceSubscriptionQuery, GetPriceSubscriptionQueryHandler
        )

        query_maps.register_query(
            GetListServerQuery, GetListServerQueryHandler
        )
        query_maps.register_query(
            GetListProtocolsQuery, GetListProtocolsQueryHandler
        )
        return query_maps

    @provide(scope=Scope.APP)
    def event_maps(self) -> EventRegisty:
        events_maps = EventRegisty()

        events_maps.subscribe(
            BaseEvent, [LogHandlerEvent]
        )

        events_maps.subscribe(
            PaidPaymentEvent, [DecrementFreeServerEventHandler]
        )
        return events_maps
