from enum import IntEnum

class OrderStatusEnum(IntEnum):
    Pending = 1
    Expired = 2
    Completed = 3
    Expedited = 4
    Timeout = 5

class WorkStatusEnum(IntEnum):
    work = 1
    idle = 2

