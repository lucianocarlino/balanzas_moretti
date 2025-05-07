from fastapi import APIRouter
from app.crud import package
from app.schemas.package import Package, PackageCreate

packages = APIRouter()

@packages.get("/packages", response_model=None)
def get_packages():
    data = package.read_all()
    return data

@packages.get("/packages/{package_id}")
def get_package(package_id: int):
    data = package.read_one(package_id)
    return data

@packages.post("/packages")
def create_package(packageCreate: PackageCreate):
    data = package.create_package(packageCreate.name, packageCreate.expected_weight, packageCreate.minimum_weight, packageCreate.maximum_weight)
    return data

@packages.delete("/packages/{package_id}")
def delete_package(package_id: int):
    data = package.delete_package(package_id)
    if data:
        return {}
    else:
        return {"message": "No se pudo eliminar el paquete"}
    
@packages.put("/packages/update/{package_id}")
def update_package(package_update: PackageCreate, package_id):
    data = package.update_package(package_update.name, package_update.expected_weight, package_update.minimum_weight, package_update.maximum_weight, package_id)
    if data:
        return {}
    else:
        return {"message": "No se pudo actualizar el paquete"}