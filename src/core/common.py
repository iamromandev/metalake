import hashlib
import json
from collections.abc import Mapping, Sequence
from datetime import UTC, datetime
from typing import Any, TypeVar

import toml

K = TypeVar("K")
V = TypeVar("V")
T = TypeVar("T")
VarTuple = tuple[V] | tuple[V, V] | tuple[V, V, V]


def get_app_version() -> str:
    try:
        with open("pyproject.toml") as f:
            data = toml.load(f)
            return data['project']['version']
    except FileNotFoundError:
        return "Version information not found"
    except KeyError:
        return "Version key not found in pyproject.toml"


def current_timestamp(format: str | None = None) -> str:
    # "%Y%m%d%H%M%S"
    dt = datetime.now(UTC)
    timestamp = dt.strftime(format) if format else dt.isoformat()
    return timestamp


def safely_deep_get(
    data: Mapping[K, V] | Sequence[V] | object,
    keys: str,
    default: T | None = None,
) -> Any | None:
    """
    Returns a value from nested dictionary/list/tuple/object using dot-separated keys.

    Args:
        data: Nested dictionary, list/tuple, or object.
        keys: Dot-separated keys, e.g., "user.profile.name".
        default: Value to return if key not found. Defaults to None.

    Returns:
        The value at the nested key path or `default` if not found.
    """
    node = data
    for key in keys.split("."):
        if isinstance(node, dict):
            node = node.get(key, None)
        elif isinstance(node, (list, tuple)) and key.isdigit():
            index = int(key)
            node = node[index] if 0 <= index < len(node) else None
        elif hasattr(node, key):
            node = getattr(node, key)
        else:
            return default

        if node is None:
            return default

    return node

 
def compute_checksum(content: dict[str, Any]) -> str:
    content_str: str = json.dumps(content, sort_keys=True)
    content_bytes: bytes = content_str.encode('utf-8')
    return hashlib.sha256(content_bytes).hexdigest()
