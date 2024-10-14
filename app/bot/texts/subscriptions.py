from domain.entities.subscription import Subscription


class SubscriptionText:
    BUY: str = """Выберите тариф"""
    NOT_ACTIVE_SUB: str = "У вас нет активных подписок."

    @staticmethod
    def get_vpn_url_text(vpn: Subscription) -> str:
        return f"""
Дата подписки: {vpn.created_at.day}\-{vpn.created_at.month}\-{vpn.created_at.year}
Дата окончания: {vpn.end_time.day}\-{vpn.end_time.month}\-{vpn.end_time.year}
Цена: {vpn.amount}
Ccылка: `{vpn.vpn_url}`"""