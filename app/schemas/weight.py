from pydantic import BaseModel
from typing import List
from app.schemas.scale import ScaleAnnouncement


class PushWeights(BaseModel):
    peso_inicial: float
    peso_final: float
    paquete: int
    ts: int

class HttpWeight(BaseModel):
    pesos: List[PushWeights]
    announcement: ScaleAnnouncement