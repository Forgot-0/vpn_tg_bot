class GuideText:
    DOWNLOAD_IOS: str = """Установка vpn на IOS и Mac проходит одинаково для этого скачиваем из App Store приложение [FoXray](https://apps.apple.com/app/id6448898396)"""
    VIDEO_IOS: str = 'CgACAgIAAxkBAANkZwvxU9DFBptW0jNhyWrOja7rLR4AAotmAAKyMWFIhCF7sF45CGk2BA'

    DOWNLOAD_WINDOWS: str = """Установка vpn на Windows скачиваем zip [nekoray](https://github.com/MatsuriDayo/nekoray/releases/download/3.26/nekoray-3.26-2023-12-09-windows64.zip)"""
    VIDEO_WINDOWS: str = ...

    DOWNLOAD_LINUX: str = """Установка vpn на Linux заходим на github [nekoray](https://github.com/MatsuriDayo/nekoray/releases) и скачивайте файл под свою систему"""
    VIDEO_LINUX: str = ...

    ROUTE_NEKORAY_SETTING: str = '`{"rules": [{"domain_suffix": [".ru"], "outbound": "direct"}]}`'