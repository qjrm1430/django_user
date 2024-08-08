import enum


class USER_ROLE(enum.Enum):
    CUST = (enum.auto, "일반고객")
    ADMIN = (enum.auto, "관리자")
