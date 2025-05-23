from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class SubscriptionStatus(str, Enum):
    expired = "expired"  # истекшая подписка (первичное отключение)
    last_day_left_expiration = "last_day_left_expiration"  # 1 день до истечения подписки (первичное отключение)
    last_two_days_left_expiration = "last_two_days_left_expiration"  # 2 дня до истечения подписки (первичное отключение)

    terminated = "terminated"  # полное удаление (терминация)
    last_day_left_termination = "last_day_left_termination"  # 1 день до терминации
    last_two_days_left_termination = "last_two_days_left_termination"  # 2 дня до терминации