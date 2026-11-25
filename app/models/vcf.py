from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class VcfFile(Base):
    __tablename__ = "vcf_files"

    id: Mapped[int] = mapped_column(primary_key=True)
    project_id: Mapped[int] = mapped_column(
        ForeignKey("projects.id", ondelete="CASCADE"), index=True
    )
    filename: Mapped[str] = mapped_column(String(255))
    file_format: Mapped[str | None] = mapped_column(String(50))
    variant_count: Mapped[int] = mapped_column(default=0)
    uploaded_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    variants: Mapped[list[Variant]] = relationship(
        back_populates="vcf_file", cascade="all, delete-orphan", passive_deletes=True
    )


class Variant(Base):
    __tablename__ = "variants"

    id: Mapped[int] = mapped_column(primary_key=True)
    vcf_file_id: Mapped[int] = mapped_column(
        ForeignKey("vcf_files.id", ondelete="CASCADE"), index=True
    )
    chrom: Mapped[str] = mapped_column(String(50))
    pos: Mapped[int]
    variant_id: Mapped[str | None] = mapped_column(String(255))
    ref: Mapped[str] = mapped_column(String)
    alt: Mapped[str] = mapped_column(String)
    qual: Mapped[float | None]
    filter: Mapped[str | None] = mapped_column(String(255))
    af: Mapped[float | None]

    vcf_file: Mapped[VcfFile] = relationship(back_populates="variants")
