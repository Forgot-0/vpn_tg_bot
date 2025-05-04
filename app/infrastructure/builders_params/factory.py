
from dataclasses import dataclass
from typing import Type
from domain.entities.server import ProtocolConfig
from domain.services.ports import BaseProtocolBuilder
from domain.values.servers import ApiType, ProtocolType


@dataclass
class ProtocolBuilderFactory:
    _registy: dict[tuple[ApiType, ProtocolType], Type[BaseProtocolBuilder]]

    def registy(
            self,
            api_type: ApiType,
            protocol_type: ProtocolType,
            builder: Type[BaseProtocolBuilder]
        ) -> None:
        self._registy[(api_type, protocol_type)] = builder

    def get(self, api_type: ApiType, protocol_config: ProtocolConfig) -> BaseProtocolBuilder:
        builder_cls = self._registy[(api_type, protocol_config.protocol_type)]

        return builder_cls(protocol_config.config)
