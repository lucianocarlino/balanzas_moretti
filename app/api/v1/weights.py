from fastapi import APIRouter
from fastapi.responses import FileResponse
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
    file_path = "weights.csv"
    return FileResponse(file_path, filename="weights.csv")


        
