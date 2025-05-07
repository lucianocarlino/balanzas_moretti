from pydantic import BaseModel

class Package(BaseModel):
    package_id: int
    name: str
    expected_weight: float
    minimum_weight: float
    maximum_weight: float

class PackageCreate(BaseModel):
    name: str
    expected_weight: float
    minimum_weight: float
    maximum_weight: float
