from collections.abc import Mapping
from typing import Final

from app.domain.values.users import UserRole



SUBORDINATE_ROLES: Final[Mapping[UserRole, set[UserRole]]] = {
    UserRole.SUPER_ADMIN: {UserRole.ADMIN, UserRole.USER},
    UserRole.ADMIN: {UserRole.USER},
    UserRole.USER: set(),
}


class RoleAccessControl:
    def can_action(self, user_role: UserRole, target_role: UserRole) -> bool:
        return target_role == user_role or target_role in SUBORDINATE_ROLES.get(user_role, set())

    def can_change_role(self, user_role: UserRole, target_role: UserRole) -> bool:
        return target_role in SUBORDINATE_ROLES.get(user_role, set())

    def is_role_assignable(self, user_role: UserRole) -> bool:
        return user_role.is_assignable

    def is_role_changeable(self, user_role: UserRole) -> bool:
        return user_role.is_changeable

