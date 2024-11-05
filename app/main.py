from fastapi import FastAPI
from services.modbusMaster import ModbusMaster

app = FastAPI()

Master = ModbusMaster(port="/dev/ttyUSB0", baudrate=9600)
Master.connect()    

@app.get("/items/{item_id}")
async def read_item(item_id: str, q: str | None = None):
    if q:
        return {"item_id": item_id, "q": q}
    return {"item_id": item_id}