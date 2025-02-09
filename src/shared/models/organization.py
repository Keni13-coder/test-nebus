from .base import Base
from src.shared.database.base import created_at, updated_at, is_active

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import VARCHAR


class Organization(Base):
    __tablename__ = "organizations"

    org_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    title: Mapped[str] = mapped_column(VARCHAR(255))
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]
    is_active: Mapped[is_active]

    categories: Mapped[list["Category"]] = relationship(
        "Category",
        secondary="works",
        back_populates="organizations"
    )

class Phone(Base):
    __tablename__ = "phones"

    phone_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    org_id: Mapped[int] = mapped_column(ForeignKey("organizations.org_id", ondelete="CASCADE"), index=True)
    phone: Mapped[str] = mapped_column(VARCHAR(255))
    