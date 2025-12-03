
from dataclasses import dataclass, field
from typing import Type
from app.domain.entities.server import ProtocolConfig
from app.domain.services.ports import BaseProtocolBuilder
from app.domain.values.servers import ApiType, ProtocolType


@dataclass
class ProtocolBuilderFactory:
    _registry: dict[tuple[ApiType, ProtocolType], Type[BaseProtocolBuilder]] = field(default_factory=dict)

    def register(
            self,
            api_type: ApiType,
            protocol_type: ProtocolType,
            builder: Type[BaseProtocolBuilder]
        ) -> None:
        self._registry[(api_type, protocol_type)] = builder

    def get(self, api_type: ApiType, protocol_type: ProtocolType) -> BaseProtocolBuilder:
        builder_cls = self._registry[(api_type, protocol_type)]

        return builder_cls(protocol_type)
