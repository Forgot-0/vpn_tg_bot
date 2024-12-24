from application.dto.profile import Profile


class ProfileMessage:
    _text = (
        "📊 Информация об активных подписках : \n\n"
    )
    _reply_markup = None

    def build(self, profiles: list[Profile]):
        for profile in profiles:
            self._text += (
                "\n"
                "👤 Логин: " + profile.id + "\n"
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
                    f"└─ 📅 {profile.end_time.date()}\n"
                )

            if profile.limit_trafic != 0:
                self._text += (
                    "\n"
                    "💾 Лимиты трафика: \n"
                    f"├─ 📦 Общий объем: {profile.limit_trafic:0.2f} ГБ"
                    f"└─ ✨ Осталось: {(profile.limit_trafic-profile.download-profile.upload):0.2f}ГБ"
                )

        content = {"text": self._text}
        return content