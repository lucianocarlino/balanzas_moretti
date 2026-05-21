from pydantic import BaseModel
from app.schemas.package import Package

class Scale(BaseModel):
    scale_id: int
    line: int
    slave_address: int
    packages: list[Package]

class ScaleCreate(BaseModel):
    name: str
    packages: list[int]
    address: int

class ScaleUpdate(BaseModel):
    name: str
    packages: list[int]

class ScaleAnnouncement(BaseModel):
    mac: str
    wifi: str
    ip: str
    status: str
    version: str
    balanza: int
    timestamp: int