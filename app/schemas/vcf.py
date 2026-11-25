from datetime import datetime

from pydantic import BaseModel, ConfigDict


class VariantRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    chrom: str
    pos: int
    variant_id: str | None
    ref: str
    alt: str
    qual: float | None
    filter: str | None
    af: float | None


class VcfFileRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    project_id: int
    filename: str
    file_format: str | None
    variant_count: int
    uploaded_at: datetime


class VcfFileDetail(VcfFileRead):
    variants: list[VariantRead]
