from typing import Any, TypeVar, Type, cast


T = TypeVar("T")


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


class Config:
    client_tile: str
    window_width: int

    def __init__(self, client_tile: str, window_width: int) -> None:
        self.client_tile = client_tile
        self.window_width = window_width

    @staticmethod
    def from_dict(obj: Any) -> 'Config':
        assert isinstance(obj, dict)
        client_tile = from_str(obj.get("client_tile"))
        window_width = from_int(obj.get("window_width"))
        return Config(client_tile, window_width)

    def to_dict(self) -> dict:
        result: dict = {}
        result["client_tile"] = from_str(self.client_tile)
        result["window_width"] = from_int(self.window_width)
        return result


def config_from_dict(s: Any) -> Config:
    return Config.from_dict(s)


def config_to_dict(x: Config) -> Any:
    return to_class(Config, x)
