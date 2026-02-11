import asyncio

from app.logs.logging_config import Logger
from app.services.weights import weights, Weights
from app.exceptions.DBException import DBException
from pymodbus.exceptions import ModbusException

rt_data = []

logger = Logger("RTData-Services").logger

async def continuos_read():
    try:
        while True:
            await weights.read_weights_from_scales()
            await asyncio.sleep(5)
    except DBException as e:
        logger.error(f'Error de base de datos en lectura continua: {e}')
        print(f"Error de base de datos en lectura continua: {e}")
    except ModbusException as e:
        logger.error(f'Error de Modbus de datos en lectura {e}')
        print(f"Error de Modbus en lectura continua: {e}")
    except asyncio.CancelledError:
        logger.error(f'Error de cancelamento de lectura continua: {e}')
        print("Continuos read task cancelled")
    except Exception as e:
        logger.error(f'Error inesperado en lectura continua: {e}')
        print(f"Error inesperado en lectura continua: {e}")
