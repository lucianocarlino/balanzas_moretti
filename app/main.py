import asyncio
import json
from app.crud.weight import read_all
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from dotenv import load_dotenv
from app.api.v1.scales import scales
from app.api.v1.weights import weights
from app.api.v1.packages import packages
from app.services.weights import weights as weights_service
from app.services.rt_data import continuos_read as rt_continuos_read
from app.services.scales import set_up_scales
from app.services.modbusMaster import Master
from app.exceptions.DBException import DBException
from pymodbus.exceptions import ModbusException
from app.logs.logging_config import Logger

app = FastAPI()

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

weight_continous_read = None
sse_task = None

logger = Logger("main").logger

async def event_generator():
    try:
        while True:
            try:
                data = read_all(1000)
                data = list(map(lambda x: x.to_dict(), data))
                yield f"event: newWeights\ndata: {data}\n\n"
            except DBException as e:
                logger.error(f"Error de base de datos en event_generator: {e}")
                print(f"Error de base de datos en event_generator: {e}")
                yield f"event: error\ndata: Error de base de datos: {str(e)}\n\n"
            except Exception as e:
                logger.error(f"Error inesperado en event_generator: {e}")
                print(f"Error inesperado en event_generator: {e}")
                yield f"event: error\ndata: Error inesperado: {str(e)}\n\n"
            await asyncio.sleep(15)
    except asyncio.CancelledError:
        logger.error("Event generator cancelled")
        print("Event generator cancelled")
        raise

async def continuos_read():
    try:
        while True:
            await weights_service.read_weights_from_scales()
            await asyncio.sleep(15)
    except asyncio.CancelledError:
        logger.error("Continuous read cancelled")
        print("Continuos read task cancelled")

@app.on_event("startup")
async def startup_event():
    try:
        logger.info("Starting event loop")
        Master.connect()
    except ModbusException as e:
        logger.error(f"Error de Modbus al conectar en startup: {e}")
        print(f"Error de Modbus al conectar en startup: {e}")
    except Exception as e:
        logger.error(f"Error inesperado al conectar en startup: {e}")
        print(f"Error inesperado al conectar en startup: {e}")
    weights_service.refresh_scales()
    for scale in weights_service.scales:
        scale.online = False
    global weight_continous_read
    weight_continous_read = asyncio.create_task(continuos_read())

@app.get("/sse")
async def sse():
    global sse_task
    sse_task = StreamingResponse(event_generator(), media_type="text/event-stream")
    return sse_task

@app.on_event("shutdown")
async def shutdown_event():
    global weight_continous_read
    global sse_task
    if weight_continous_read:
        weight_continous_read.cancel()
    try:
        logger.info("Shutdown event loop")
        Master.close()
    except ModbusException as e:
        print(f"Error de Modbus al cerrar conexión: {e}")
    except Exception as e:
        print(f"Error inesperado al cerrar conexión: {e}")

app.include_router(scales)  
app.include_router(packages)
app.include_router(weights)

load_dotenv()

@app.get("/")
async def read_root():
    # await Master.connect()
    return {"message": "Welcome"}
