from app.services.modbusMaster import Master
import datetime
from app.crud.scale import read_all
from pymodbus.exceptions import ModbusException

def find_scales():
    scales = []
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
    return scales

def set_up_scales(scales):
    for scale in scales:
        try:
            print(f"Setting up scale address {scale.slave_address}")
            Master.load_packages(scale.slave_address, scale.packages)
            scale.online = True
        except ModbusException as e:
            print(f"Error de Modbus configurando scale {scale.slave_address}: {e}")
            scale.online = False
        except Exception as e:
            print(f"Error inesperado configurando scale {scale.slave_address}: {e}")
            scale.online = False
