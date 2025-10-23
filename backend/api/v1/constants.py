from enum import StrEnum


class ChannelGroup(StrEnum):
    NOTIFICATION = 'notification_v1'
    PERSONAL = 'user_v1_{}'
