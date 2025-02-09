from .base import Base

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import VARCHAR



class Work(Base):
    '''secondary table'''
    
    __tablename__ = "works"

    work_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.category_id"), index=True)
    org_id: Mapped[int] = mapped_column(ForeignKey("organizations.org_id"), index=True)
    
    
class Category(Base):
    __tablename__ = "categories"

    category_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    title: Mapped[str] = mapped_column(VARCHAR(255))
    path: Mapped[str] = mapped_column(VARCHAR(255))

    organizations: Mapped[list["Organization"]] = relationship(
        "Organization",
        secondary="works",
        back_populates="categories"
    )