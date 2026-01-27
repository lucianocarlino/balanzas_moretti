import io
import csv
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from app.crud import weight
from app.services.weights import weights
from app.services.rt_data import rt_data
from app.exceptions.DBException import DBException

weights = APIRouter()

@weights.get("/weights", response_model=None)
def get_weights(limit: int = 1000, init: str = None, end: str = None, package_id: int = None, scale_id: int = None):
    try:
        data = weight.read_all(limit, init, end, package_id, scale_id)
        return data
    except DBException as e:
        print(f"Error de base de datos al obtener pesos: {e}")
        raise HTTPException(status_code=500, detail=f"Error de base de datos: {str(e)}")
    except Exception as e:
        print(f"Error inesperado al obtener pesos: {e}")
        raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")

@weights.get("/weights/download", response_model=None)
def download_weights():
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
        print(f"Error de base de datos al descargar pesos: {e}")
        raise HTTPException(status_code=500, detail=f"Error de base de datos: {str(e)}")
    except Exception as e:
        print(f"Error inesperado al descargar pesos: {e}")
        raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")



