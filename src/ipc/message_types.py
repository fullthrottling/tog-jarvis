from enum import Enum, auto


class MessageType(Enum):
    SIZE_CHANGE = auto()
    STATUS_UPDATE = auto()
    ERROR = auto()
    # 필요한 경우 더 많은 메시지 타입을 추가하세요
