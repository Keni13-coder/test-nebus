from .base import Base
from src.shared.config.settings import settings

from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import VARCHAR
from geoalchemy2 import Geography


class Office(Base):
    __tablename__ = "offices"

    office_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    address: Mapped[str] = mapped_column(VARCHAR(255))
    org_id: Mapped[int] = mapped_column(ForeignKey("organizations.org_id", ondelete="CASCADE"), index=True, unique=True)


class Geo(Base):
    __tablename__ = "geo"

    geo_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    office_id: Mapped[int] = mapped_column(ForeignKey("offices.office_id", ondelete="CASCADE"), index=True, unique=True)
    geog: Mapped[Geography] = mapped_column(Geography(geometry_type="POINT", srid=settings.SRID_GEO), comment="WGS84")
