import io
import csv
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import StreamingResponse
from app.crud import weight
from app.logs.logging_config import Logger
from app.services.weights import weights as weightsService
from app.services.rt_data import rt_data
from app.exceptions.DBException import DBException
from app.schemas.weight import PushWeights, HttpWeight
from typing import List

weights = APIRouter()
logger = Logger("Weights-api").logger

@weights.get("/weights", response_model=None)
def get_weights(limit: int = 1000, init: str = None, end: str = None, package_id: int = None, scale_id: int = None):
    try:
        data = weight.read_all(limit, init, end, package_id, scale_id)
        return data
    except DBException as e:
        logger.error(f'Error de base de datos al obtener pesos: {e}')
        print(f"Error de base de datos al obtener pesos: {e}")
        raise HTTPException(status_code=500, detail=f"Error de base de datos: {str(e)}")
    except Exception as e:
        logger.error(f'Error inesperado al obtener pesos: {e}')
        print(f"Error inesperado al obtener pesos: {e}")
        raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")

@weights.get("/weights/download", response_model=None)
def download_weights():
    logger.info("Iniciando descarga de pesos")
    try:
        data = weight.read_all()
        if not data:
            csv_bytes = b""
        else:
            headers = list(data[0].to_dict().keys())
            buf = io.StringIO()
            writer = csv.writer(buf)
            writer.writerow(headers)
            for item in data:
                writer.writerow([item.to_dict().get(h, "") for h in headers])
            csv_bytes = buf.getvalue().encode("utf-8")

        return StreamingResponse(
            io.BytesIO(csv_bytes),
            media_type="text/csv",
            headers={"Content-Disposition": 'attachment; filename="weights.csv"'}
        )
    except DBException as e:
        logger.error(f'Error de base de datos al descargar pesos: {e}')
        print(f"Error de base de datos al descargar pesos: {e}")
        raise HTTPException(status_code=500, detail=f"Error de base de datos: {str(e)}")
    except Exception as e:
        logger.error(f'Error inesperado al descargar pesos: {e}')
        print(f"Error inesperado al descargar pesos: {e}")
        raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")

@weights.post("/weights/push_weights")
def push_weights(pushweights: HttpWeight):
    try:
        weightsService.process_http_weight(pushweights)
    except DBException as e:
        logger.error(f'Error de base de datos al push weights: {e}')
        print(f"Error de base de datos al push weights: {e}")
        raise HTTPException(status_code=500, detail=f"Error de base de datos: {str(e)}")
    except Exception as e:
        logger.error(f'Error inesperado al push weights: {e}')
        print(f"Error inesperado al push weights: {e}")
        raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")
