
from dataclasses import asdict
import json
from typing import Any



def convert_dict_in_json(data: dict[str, Any]) -> str:
    return json.dumps(data)

def convert_str_in_json(data: str) -> dict[str, str]:
    return json.loads(data)