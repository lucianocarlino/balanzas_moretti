from fastapi import APIRouter, HTTPException
from app.crud import package
from app.schemas.package import Package, PackageCreate
from app.exceptions.DBException import DBException
from pymodbus.exceptions import ModbusException

packages = APIRouter()

@packages.get("/packages", response_model=None)
def get_packages():
    try:
        data = package.read_all()
        return data
    except DBException as e:
        print(f"Error de base de datos al obtener paquetes: {e}")
        raise HTTPException(status_code=500, detail=f"Error de base de datos: {str(e)}")
    except Exception as e:
        print(f"Error inesperado al obtener paquetes: {e}")
        raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")

@packages.get("/packages/{package_id}")
def get_package(package_id: int):
    try:
        data = package.read_one(package_id)
        return data
    except DBException as e:
        print(f"Error de base de datos al obtener paquete {package_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Error de base de datos: {str(e)}")
    except Exception as e:
        print(f"Error inesperado al obtener paquete {package_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")

@packages.post("/packages")
def create_package(packageCreate: PackageCreate):
    try:
        data = package.create_package(packageCreate.name, packageCreate.expected_weight, packageCreate.minimum_weight, packageCreate.maximum_weight)
        return data
    except DBException as e:
        print(f"Error de base de datos al crear paquete: {e}")
        raise HTTPException(status_code=500, detail=f"Error de base de datos: {str(e)}")
    except Exception as e:
        print(f"Error inesperado al crear paquete: {e}")
        raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")

@packages.delete("/packages/{package_id}")
def delete_package(package_id: int):
    try:
        data = package.delete_package(package_id)
        if data:
            return {}
        else:
            return {"message": "No se pudo eliminar el paquete"}
    except DBException as e:
        print(f"Error de base de datos al eliminar paquete {package_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Error de base de datos: {str(e)}")
    except Exception as e:
        print(f"Error inesperado al eliminar paquete {package_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")

@packages.put("/packages/update/{package_id}")
def update_package(package_update: PackageCreate, package_id):
    try:
        data = package.update_package(package_update.name, package_update.expected_weight, package_update.minimum_weight, package_update.maximum_weight, package_id)
        if data:
            return {}
        else:
            return {"message": "No se pudo actualizar el paquete"}
    except DBException as e:
        print(f"Error de base de datos al actualizar paquete {package_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Error de base de datos: {str(e)}")
    except ModbusException as e:
        print(f"Error de comunicación Modbus al actualizar paquete {package_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Error de comunicación Modbus: {str(e)}")
    except Exception as e:
        print(f"Error inesperado al actualizar paquete {package_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")

@packages.put("/packages/restore/{package_id}")
def restore_package(package_id: int):
    try:
        data = package.restore_package(package_id)
        if data:
            return {"message": "Package restored"}
        else:
            return {"message": "Package not found"}
    except DBException as e:
        print(f"Error de base de datos al restaurar paquete {package_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Error de base de datos: {str(e)}")
    except Exception as e:
        print(f"Error inesperado al restaurar paquete {package_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")


