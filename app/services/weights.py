from app.crud import scale
from app.db.base import session
from app.logs.logging_config import Logger
from app.schemas.scale import ScaleAnnouncement
from app.models.scale import Scale
from app.schemas.weight import HttpWeight
from app.services.modbusMaster import Master
from app.services.scales import set_up_http_scale, heartbeat_http_scale
from app.crud.weight import write_weight, write_http_weight
from app.exceptions.DBException import DBException
from pymodbus.exceptions import ModbusException
import pandas as pd

class Weights:
    def __init__(self):
        self.scales = scale.read_all()
        self.scales_availables = []
        self.logger = Logger("Weights-Services").logger

    async def read_weights_from_scales(self):
        weights = []
        for scale in self.scales:
            try:
                if scale.comunicacion != "HTTP":
                    weights_from_scale = Master.read_weights_from_scale(scale)
                    if Master.connected:
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
                    else:
                        Master.connect()
                else:
                    scale.online = heartbeat_http_scale(scale)

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
        return weights
    
    def refresh_scales(self):
        try:
            self.scales = scale.read_all()
        except DBException as e:
            print(f"Error de base de datos al refrescar balanzas: {e}")
        except Exception as e:
            print(f"Error inesperado al refrescar balanzas: {e}")

    def set_http_scale(self, http_scale: ScaleAnnouncement):
        try:
            agregado = False
            for _scale in self.scales:
                if _scale.slave_address == http_scale.balanza:
                    _scale.comunicacion = "HTTP"
                    _scale.online = True
                    _scale.active = True
                    _scale.ip = http_scale.ip
                    _scale.mac = http_scale.mac
                    session.commit()
                    set_up_http_scale(_scale, http_scale)
                    self.logger.info(f'Balanza {http_scale.balanza} establecida como HTTP con IP {http_scale.ip} y MAC {http_scale.mac}')
                    agregado = True
            if not agregado:
                self.scales_availables.append(http_scale.balanza)
        except Exception as e:
            print(f'Error inesperado al establecer como http la balanza {http_scale.balanza}: {e}')
            self.logger.error(f'Error inesperado al establecer como http la balanza {http_scale.balanza}: {e}')

    def process_http_weight(self,  weights: HttpWeight):
        try:
            scale_obj = session.query(Scale).filter(Scale.scale_id == weights.announcement.balanza).first()
            if scale_obj.comunicacion != "HTTP":
                self.set_http_scale(weights.announcement)
            write_http_weight(weights, scale_obj)
        except DBException as e:
            print(f"Error de base de datos al escribir pesos HTTP: {e}")
            self.logger.error(f"Error de base de datos al escribir pesos HTTP: {e}")
        except Exception as e:
            print(f"Error inesperado al escribir pesos HTTP: {e}")
            self.logger.error(f"Error inesperado al escribir pesos HTTP: {e}")



weights = Weights()
            
def generate_csv(weights : list[Weights]):
    weights_data = [weight.to_dict() for weight in weights]
    df = pd.DataFrame(weights_data)
    df.to_csv("weights.csv", index=False)


