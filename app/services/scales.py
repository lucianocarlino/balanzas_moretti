from app.logs.logging_config import Logger
from app.schemas.scale import Scale, ScaleAnnouncement
from app.services.modbusMaster import Master
from app.models.scale import Scale as ModelScale
import datetime
from app.crud.scale import read_all, read_one, get_scale_packages
from pymodbus.exceptions import ModbusException
from app.services.httpScale import HttpScale

logger = Logger("Scales-Services").logger

def find_scales():
    scales = []
    logger.info("Iniciando búsqueda de balanzas")
    try:
        Master.connect()
    except ModbusException as e:
        print(f"Error de Modbus al conectar: {e}")
        return [-1]
    except Exception as e:
        print(f"Error inesperado al conectar: {e}")
        return [-1]

    if Master.connected:
        for slave in range(1, 15):
            print(f'Buscando en el slave {slave}')
            print(f'DateTime: {datetime.datetime.now()}')
            try:
                result = Master.read_input_registers(0, slave)
                if result is not None:
                    print(f"Slave {slave} found")
                    scales.append(slave)
            except ModbusException as e:
                print(f"Slave {slave} not found (Modbus error)")
                continue
            except Exception as e:
                print(f"Slave {slave} not found")
                continue
    if len(scales) == 0:
        scales = [-1]
    logger.info(f'Encontradas: {scales}')
    return scales

def set_up_scales(scales):
    logger.info(f'Configurando balanzas: {scales}')
    for scale in scales:
        try:
            print(f"Setting up scale address {scale.slave_address}")
            Master.load_packages(scale.slave_address, scale.packages)
            scale.online = True
            logger.info(f'Balanza {scale.slave_address} configurada correctamente')
        except ModbusException as e:
            logger.error(f'Error configurando balanza con direccion {scale.slave_address}: {e}')
            print(f"Error de Modbus configurando scale {scale.slave_address}: {e}")
            scale.online = False
        except Exception as e:
            logger.error(f'Error inesperado configurando balanza con direccion {scale.slave_address}: {e}')
            print(f"Error inesperado configurando scale {scale.slave_address}: {e}")
            scale.online = False

def set_up_http_scale(scale: Scale):
    logger.info(f'Configurando balanza: {scale.scale_id}')
    try:
        HttpScale.load_packages(scale)
        logger.info(f'Balanza numero {scale.scale_id} configurada correctamente')
    except Exception as e:
        logger.error(f'Error inesperado configurando balanza numero {scale.balanza}: {e}')

def heartbeat_http_scale(scale: ModelScale):
    try:
        return HttpScale.get_status(scale)
    except Exception as e:
        logger.error(f'Balanza {scale.slave_address} desconectada: {e}')