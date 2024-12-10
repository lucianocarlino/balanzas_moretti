import asyncio
from fastapi import FastAPI
from app.services.scale import Scale
from app.services.modbusMaster import ModbusMaster
import os
from dotenv import load_dotenv

app = FastAPI()

load_dotenv()
num_scales = int(os.getenv("NUMERO_LINEAS"))
Scales = [Scale(i) for i in range(num_scales)]

Master = ModbusMaster(port="/dev/ttyUSB0", baudrate=9600)

@app.get("/")
async def read_root():
    await Master.connect()
    return {"message": "Welcome"}