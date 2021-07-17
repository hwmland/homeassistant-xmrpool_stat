"""Helper methods"""


def DefaultTo(value: str, default: str) -> str:
    return value if value != None else default


def GetDictValue(source: dict, key: str) -> any:
    if source is None:
        return None
    return source.get(key)
