from dataclasses import dataclass
from enum import Enum


class LoadingStrategyType(str, Enum):
    LAZY = "lazy"
    JOINED = "joined"
    SELECTIN = "selectin"
    SUBQUERY = "subquery"
    IMMEDIATE = "immediate"


@dataclass(frozen=True)
class RelationshipLoading:
    relationship_name: str
    strategy: LoadingStrategyType = LoadingStrategyType.LAZY
    nested: tuple["RelationshipLoading", ...] | None  = None

    @property
    def has_nested(self) -> bool:
        return self.nested is not None and len(self.nested) > 0

    @classmethod
    def lazy(cls, relationship_name: str) -> "RelationshipLoading":
        return cls(relationship_name=relationship_name, strategy=LoadingStrategyType.LAZY)

    @classmethod
    def joined(
        cls,
        relationship_name: str,
        nested: tuple["RelationshipLoading", ...] | None = None
    ) -> "RelationshipLoading":
        return cls(relationship_name=relationship_name, strategy=LoadingStrategyType.JOINED, nested=nested)

    @classmethod
    def selectin(
        cls,
        relationship_name: str,
        nested: tuple["RelationshipLoading", ...] | None = None
    ) -> "RelationshipLoading":
        return cls(relationship_name=relationship_name, strategy=LoadingStrategyType.SELECTIN, nested=nested)

    @classmethod
    def subquery(
        cls,
        relationship_name: str,
        nested: tuple["RelationshipLoading", ...] | None = None
    ) -> "RelationshipLoading":
        return cls(relationship_name=relationship_name, strategy=LoadingStrategyType.SUBQUERY, nested=nested)


@dataclass(frozen=True)
class LoadingConfig:
    relationships: tuple[RelationshipLoading, ...]

    @classmethod
    def default(cls) -> "LoadingConfig":
        return cls(relationships=())

    @classmethod
    def eager_all(
        cls,
        *relationship_names: str,
        strategy: LoadingStrategyType = LoadingStrategyType.SELECTIN
    ) -> "LoadingConfig":
        return cls(
            relationships=tuple(
                RelationshipLoading(name, strategy)
                for name in relationship_names
            )
        )

    def get_relationship(self, name: str) -> RelationshipLoading | None:
        for rel in self.relationships:
            if rel.relationship_name == name:
                return rel
        return None

    def should_load(self, name: str) -> bool:
        rel = self.get_relationship(name)
        return rel is not None and rel.strategy != LoadingStrategyType.LAZY

