from fastapi import APIRouter
from app.crud import scale
from app.schemas.scale import Scale as schemaScale, ScaleCreate, ScaleUpdate
from app.models.scale import Scale
from app.models.scales_has_packages import ScaleHasPackages
from app.models.weight import Weight
from app.models.package import Package
from app.services.scales import find_scales

scales = APIRouter()

@scales.get("/scales", response_model=None)
def get_scales():
    data = scale.read_all()
    return data

@scales.get("/scales/{scale_id}", response_model=None)
def get_scale(scale_id: int):
    data = scale.read_one(scale_id)
    return data

@scales.get("/scales_availables", response_model=None)
def get_available_addresses():
    data = find_scales()
    print(data)
    return data

@scales.post("/scales")
def create_scale(scaleCreate: ScaleCreate):
    data = scale.create_scale(scaleCreate.name, scaleCreate.packages, scaleCreate.address)
    return data

@scales.put("/scales/update/{scale_id}")
def update_scale(scaleUpdate: ScaleUpdate, scale_id):
    data = scale.update_scale(scaleUpdate.name, scaleUpdate.packages, scale_id)
    return data

@scales.delete("/scales/{scale_id}")
def delete_scale(scale_id: int):
    data = scale.delete_scale(scale_id)
    if data:
        return {"message": "Scale deleted"}
    else:
        return {"message": "Scale not found"}
