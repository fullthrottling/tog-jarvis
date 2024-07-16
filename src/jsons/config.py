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
    client_title: str
    reference_width: int
    reference_height: int

    def __init__(self, client_title: str, reference_width: int, reference_height: int) -> None:
        self.client_title = client_title
        self.reference_width = reference_width
        self.reference_height = reference_height

    @staticmethod
    def from_dict(obj: Any) -> 'Config':
        assert isinstance(obj, dict)
        client_title = from_str(obj.get("client_title"))
        reference_width = from_int(obj.get("reference_width"))
        reference_height = from_int(obj.get("reference_height"))
        return Config(client_title, reference_width, reference_height)

    def to_dict(self) -> dict:
        result: dict = {}
        result["client_title"] = from_str(self.client_title)
        result["reference_width"] = from_int(self.reference_width)
        result["reference_height"] = from_int(self.reference_height)
        return result


def config_from_dict(s: Any) -> Config:
    return Config.from_dict(s)


def config_to_dict(x: Config) -> Any:
    return to_class(Config, x)
