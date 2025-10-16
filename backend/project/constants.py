from enum import StrEnum


class ChannelGroup(StrEnum):
    NOTIFICATION = 'notification'
    PERSONAL = 'user_{}'
