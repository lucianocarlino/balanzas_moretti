import io
import csv
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from app.crud import weight
from app.services.weights import weights
from app.services.rt_data import rt_data

weights = APIRouter()

@weights.get("/weights", response_model=None)
def get_weights(limit: int = 1000, init: str = None, end: str = None, package_id: int = None, scale_id: int = None):
    data = weight.read_all(limit, init, end, package_id, scale_id)
    return data

@weights.get("/weights/download", response_model=None)
def download_weights():
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


        
