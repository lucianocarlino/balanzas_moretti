import asyncio
from app.services.weights import weights, Weights

rt_data = []

async def continuos_read():
    try:
        while True:
            await weights.read_weights_from_scales()
            await asyncio.sleep(5)
    except asyncio.CancelledError:
        print("Continuos read task cancelled")