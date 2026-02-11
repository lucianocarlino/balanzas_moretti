from fastapi import APIRouter, HTTPException
from app.crud import scale
from app.schemas.scale import Scale as schemaScale, ScaleCreate, ScaleUpdate
from app.models.scale import Scale
from app.models.scales_has_packages import ScaleHasPackages
from app.models.weight import Weight
from app.models.package import Package
from app.services.scales import find_scales
from app.exceptions.DBException import DBException
from pymodbus.exceptions import ModbusException

scales = APIRouter()
logger = Logger("Scales-api").logger

@scales.get("/scales", response_model=None)
def get_scales():
    try:
        data = scale.read_all()
        return data
    except DBException as e:
        logger.error(f"Error de base de datos al obtener balanzas: {e}")
        print(f"Error de base de datos al obtener balanzas: {e}")
        raise HTTPException(status_code=500, detail=f"Error de base de datos: {str(e)}")
    except Exception as e:
        logger.error(f"Error inesperado al obtener balanzas: {e}")
        print(f"Error inesperado al obtener balanzas: {e}")
        raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")

@scales.get("/scales/{scale_id}", response_model=None)
def get_scale(scale_id: int):
    try:
        data = scale.read_one(scale_id)
        return data
    except DBException as e:
        logger.error(f"Error de base de datos al obtener balanza {scale_id}: {e}")
        print(f"Error de base de datos al obtener balanza {scale_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Error de base de datos: {str(e)}")
    except Exception as e:
        logger.error(f"Error inesperado al obtener balanza {scale_id}: {e}")
        print(f"Error inesperado al obtener balanza {scale_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")

@scales.get("/scales_availables", response_model=None)
def get_available_addresses():
    try:
        data = find_scales()
        print(data)
        return data
    except ModbusException as e:
        logger.error(f'Error de comunicación Modbus al buscar balanzas disponibles: {e}')
        print(f"Error de comunicación Modbus al buscar balanzas disponibles: {e}")
        raise HTTPException(status_code=500, detail=f"Error de comunicación Modbus: {str(e)}")
    except Exception as e:
        logger.error(f"Error inesperado al buscar balanzas disponibles: {e}")
        print(f"Error inesperado al buscar balanzas disponibles: {e}")
        raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")

@scales.post("/scales")
def create_scale(scaleCreate: ScaleCreate):
    try:
        data = scale.create_scale(scaleCreate.name, scaleCreate.packages, scaleCreate.address)
        return data
    except DBException as e:
        logger.error(f"Error de base de datos al crear balanza: {e}")
        print(f"Error de base de datos al crear balanza: {e}")
        raise HTTPException(status_code=500, detail=f"Error de base de datos: {str(e)}")
    except ModbusException as e:
        logger.error(f"Error de comunicacion Modbus al crear balanza: {e}")
        print(f"Error de comunicación Modbus al crear balanza: {e}")
        raise HTTPException(status_code=500, detail=f"Error de comunicación Modbus: {str(e)}")
    except Exception as e:
        logger.error(f'Error inesperado al crear balanza: {e}')
        print(f"Error inesperado al crear balanza: {e}")
        raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")

@scales.put("/scales/update/{scale_id}")
def update_scale(scaleUpdate: ScaleUpdate, scale_id):
    try:
        data = scale.update_scale(scaleUpdate.name, scaleUpdate.packages, scale_id)
        return data
    except DBException as e:
        logger.error(f"Error de base de datos al actualizar balanza: {e}")
        print(f"Error de base de datos al actualizar balanza {scale_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Error de base de datos: {str(e)}")
    except ModbusException as e:
        logger.error(f"Error de comunicación Modbus al actualizar balanza {scale_id}: {e}")
        print(f"Error de comunicación Modbus al actualizar balanza {scale_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Error de comunicación Modbus: {str(e)}")
    except Exception as e:
        logger.error(f'Error inesperado al actualizar balanza: {e}')
        print(f"Error inesperado al actualizar balanza {scale_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")

@scales.delete("/scales/{scale_id}")
def delete_scale(scale_id: int):
    try:
        data = scale.delete_scale(scale_id)
        if data:
            return {"message": "Scale deleted"}
        else:
            return {"message": "Scale not found"}
    except DBException as e:
        logger.error(f"Error de base de datos al actualizar balanza: {e}")
        print(f"Error de base de datos al eliminar balanza {scale_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Error de base de datos: {str(e)}")
    except Exception as e:
        logger.error(f'Error inesperado al eliminar balanza: {e}')
        print(f"Error inesperado al eliminar balanza {scale_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")

@scales.put("/scales/restore/{scale_id}")
def restore_scale(scale_id: int):
    try:
        logger.info(f"Intentando restaurar balanza con ID {scale_id}")
        data = scale.restore_scale(scale_id)
        if data:
            return {"message": "Scale restored"}
        else:
            return {"message": "Scale not found"}
    except DBException as e:
        logger.error(f"Error de base de datos al restaurar balanza: {e}")
        print(f"Error de base de datos al restaurar balanza {scale_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Error de base de datos: {str(e)}")
    except Exception as e:
        logger.error(f'Error inesperado al restaurar balanza: {e}')
        print(f"Error inesperado al restaurar balanza {scale_id}: {e}")
        raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")


