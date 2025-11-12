from enum import StrEnum


class ChannelGroup(StrEnum):
    NOTIFICATION = "notification"
    PERSONAL = "user_{}"


class EventEnum(StrEnum):
    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"


if __name__ == "__main__":
    print(map(str, list(EventEnum)))
