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

        'uri_login': server.uri_login,
        'uri_create': server.uri_create,
        'uri_delete': server.uri_delete,
        'uri_update': server.uri_update,
        'uri_get': server.uri_get
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

        uri_login=document['uri_login'],
        uri_create=document['uri_create'],
        uri_delete=document['uri_delete'],
        uri_update=document['uri_update'],
        uri_get=document['uri_get'],
    )

