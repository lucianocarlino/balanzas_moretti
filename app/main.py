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

async def event_generator():
    try:
        while True:
            data = read_all(1000)
            data = list(map(lambda x: x.to_dict(), data))
            yield f"event: newWeights\ndata: {data}\n\n"
            await asyncio.sleep(15)
    except asyncio.CancelledError:
        print("Event generator cancelled")
        raise

async def continuos_read():
    try:
        while True:
            await weights_service.read_weights_from_scales()
            await asyncio.sleep(15)
    except asyncio.CancelledError:
        print("Continuos read task cancelled")

@app.on_event("startup")
async def startup_event():
    Master.connect()
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
    Master.close() 

app.include_router(scales)  
app.include_router(packages)
app.include_router(weights)

load_dotenv()

@app.get("/")
async def read_root():
    # await Master.connect()
    return {"message": "Welcome"}
