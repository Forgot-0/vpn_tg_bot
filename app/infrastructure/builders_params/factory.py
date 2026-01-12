
from dataclasses import dataclass, field
from typing import Type
from app.domain.entities.server import ProtocolConfig
from app.domain.services.ports import ProtocolBuilder
from app.domain.values.servers import ApiType, ProtocolType


@dataclass
class ProtocolBuilderFactory:
    _registry: dict[tuple[ApiType, ProtocolType], Type[ProtocolBuilder]] = field(default_factory=dict)

    def register(
            self,
            api_type: ApiType,
            protocol_type: ProtocolType,
            builder: Type[ProtocolBuilder]
        ) -> None:
        self._registry[(api_type, protocol_type)] = builder

    def get(self, api_type: ApiType, protocol_type: ProtocolType) -> ProtocolBuilder:
        key = (api_type, protocol_type)

        if key not in self._registry:
            raise

        builder_cls = self._registry[key]

        return builder_cls(protocol_type)
