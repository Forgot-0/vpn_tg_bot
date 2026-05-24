from enum import StrEnum


class UserRole(StrEnum):
    OWNER = "owner"
    SUPER_ADMIN = "super_admin"
    ADMIN = "admin"
    USER = "user"

    @property
    def is_assignable(self) -> bool:
        return self not in {UserRole.OWNER, UserRole.SUPER_ADMIN}

    @property
    def is_changeable(self) -> bool:
        return self not in {UserRole.OWNER, UserRole.SUPER_ADMIN}

    @property
    def is_staff(self) -> bool:
        return self in {UserRole.OWNER, UserRole.SUPER_ADMIN, UserRole.ADMIN}
