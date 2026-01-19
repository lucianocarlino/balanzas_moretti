import asyncio
from app.services.weights import weights, Weights
from app.exceptions.DBException import DBException
from pymodbus.exceptions import ModbusException

rt_data = []

async def continuos_read():
    try:
        while True:
            await weights.read_weights_from_scales()
            await asyncio.sleep(5)
    except DBException as e:
        print(f"Error de base de datos en lectura continua: {e}")
    except ModbusException as e:
        print(f"Error de Modbus en lectura continua: {e}")
    except asyncio.CancelledError:
        print("Continuos read task cancelled")
    except Exception as e:
        print(f"Error inesperado en lectura continua: {e}")
