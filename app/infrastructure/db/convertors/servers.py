from typing import Any

from domain.entities.server import Country, Server


def convert_server_entity_to_dict(server: Server) -> dict[str, Any]:
    return {
        '_id': server.id,
        'ip': server.ip,
        'port': server.port,
        'domain': server.domain,
        'limit': server.limit,
        'pbk': server.pbk,
        'country': server.country.value,
        'free': server.free,

        'name': server.name,
        'panel_port': server.panel_port,
        'panel_path': server.panel_path
    }

def convert_server_dict_to_entity(document: dict[str, Any]) -> Server:
    return Server(
        id=document['_id'],
        ip=document['ip'],
        port=document['port'],
        domain=document['domain'],
        limit=document['limit'],
        pbk=document['pbk'],
        country=Country(document['country']),
        free=document['free'],

        name=document['name'],
        panel_port=document['panel_port'],
        panel_path=document['panel_path']
    )

