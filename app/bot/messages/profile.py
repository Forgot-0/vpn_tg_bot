from application.dto.profile import ProfileDTO


class ProfileMessage:
    _text = (
        "```📊 Информация об активных подписках : \n\n"
    )
    _reply_markup = None

    def build(self, profile: ProfileDTO):
        
        self._text += (
            "\n"
            f"👤 Логин: `{profile.id}` \n"
            "\n"
            "📈 Использование трафика:\n"
            f"├─ ↑ Отправлено: {profile.upload:0.2f} ГБ\n"
            f"├─ ↓ Получено: {profile.download:0.2f} ГБ\n"
            f"└─ 📊 Всего: {(profile.download+profile.upload):0.2f} ГБ\n"
        )

        if profile.end_time.year != 1970:
            self._text += (
                "\n"
                "⏳ Срок действия до:\n"
                f"└─ 📅 {profile.end_time.day}\-{profile.end_time.month}\-{profile.end_time.year} \n"
            )

        if profile.limit_trafic != 0:
            self._text += (
                "\n"
                "💾 Лимиты трафика: \n"
                f"├─ 📦 Общий объем: {profile.limit_trafic:0.2f} ГБ \n"
                f"└─ ✨ Осталось: {(profile.limit_trafic-profile.download-profile.upload):0.2f}ГБ \n"
            )

        self._text += '```'
        self._text += (
            "Ссылка на vpn: "
            f"`{profile.vpn_url}`"
        )

        content = {"text": self._text}
        content['parse_mode'] = "MarkdownV2"
        return content