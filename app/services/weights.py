from app.crud import scale
from app.db.base import session
from app.logs.logging_config import Logger
from app.services.modbusMaster import Master
from app.crud.weight import write_weight
from app.exceptions.DBException import DBException
from pymodbus.exceptions import ModbusException
import pandas as pd

class Weights:
    def __init__(self):
        self.scales = scale.read_all()
        self.logger = Logger("Weights-Services").logger

    async def read_weights_from_scales(self):
        weights = []
        if Master.connected:
            for scale in self.scales:
                try:
                    weights_from_scale = Master.read_weights_from_scale(scale)
                    if weights_from_scale == None:
                        scale.online = False
                        pass
                    else:
                        if scale.online == True:
                            weights.append(weights_from_scale)
                        else:
                            scale.online = True
                            Master.load_packages(scale.slave_address, scale.packages)
                            pass
                except ModbusException as e:
                    self.logger.error(f'Error de Modbus leyendo pesos de scale {scale.name}: {e}')
                    print(f"Error de Modbus leyendo pesos de scale {scale.name}: {e}")
                    scale.online = False
                except Exception as e:
                    self.logger.error(f'Error inesperado leyendo pesos de scale {scale.name}: {e}')
                    print(f"Error inesperado leyendo pesos de scale {scale.name}: {e}")
                    scale.online = False
            try:
                update_packages = write_weight(weights)
                if len(update_packages) > 0:
                    for scale in self.scales:
                        if scale.scale_id in update_packages:
                            Master.load_packages(scale.slave_address, scale.packages)
                            self.logger.info(f"Paquetes actualizados en la balanza {scale.name} con address {scale.slave_address}.")
                            print(f"Paquetes actualizados en las balanza {scale.name} con address {scale.slave_address}.")
            except DBException as e:
                Master.load_packages()
                self.logger.error(f"Error de base de datos al escribir pesos: {e}")
                print(f"Error de base de datos al escribir pesos: {e}")
            except Exception as e:
                self.logger.error(f"Error de base de datos al escribir pesos: {e}")
                print(f"Error inesperado al escribir pesos: {e}")
        else:
            Master.connect()
        return weights
    
    def refresh_scales(self):
        try:
            self.scales = scale.read_all()
        except DBException as e:
            print(f"Error de base de datos al refrescar balanzas: {e}")
        except Exception as e:
            print(f"Error inesperado al refrescar balanzas: {e}")

weights = Weights()
            
def generate_csv(weights : list[Weights]):
    weights_data = [weight.to_dict() for weight in weights]
    df = pd.DataFrame(weights_data)
    df.to_csv("weights.csv", index=False)


