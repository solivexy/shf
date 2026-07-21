import math
from typing import Any

def clean_json_floats(obj: Any) -> Any:
    """
    Recursively replaces float('nan') and float('inf') with None
    so that they can be safely serialized to standard JSON.
    """
    if isinstance(obj, float):
        if math.isnan(obj) or math.isinf(obj):
            return None
        return obj
    elif isinstance(obj, dict):
        return {k: clean_json_floats(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [clean_json_floats(x) for x in obj]
    return obj
