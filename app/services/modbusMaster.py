import asyncio
import pymodbus.client as ModbusClient
from pymodbus.exceptions import ModbusException
import numpy as np
from app.models.package import Package
from app.crud import scale
from app.models.scale import Scale
from datetime import datetime
from pytz import timezone

class ModbusMaster:

    _instance = None

    def __init__(self, port, baudrate=115200, timeout=0.2):
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout       
        self.connected = False 

    def connect(self):
        if not self.connected:
            self.client = ModbusClient.ModbusSerialClient(port=self.port, baudrate=self.baudrate, timeout=self.timeout, retries=3)
            try:
                self.client.connect()
                if self.client.connected:
                    self.connected = True
                    print("Connection success")
                else:
                    self.connected = False
                    print("Connection failed")
            except ModbusException as e:
                print("File not found")
                self.connected = False
            except Exception as e:
                print("catch")
                self.connected = False

    
    def close(self):
        if self.client.connected:
            self.connected = False
            self.client.close()

    def reconnect(self):
        self.client.close()
        self.connect()

    async def read_registers(self, slave, address, count, unit=1):
        try:
            response = await self.client.protocol.read_holding_registers(address, count, slave=slave, unit=unit)
            if response.isError():
                raise ModbusException("Error reading registers")
            return response.registers
        except ModbusException as e:
            print(f"Modbus error: {e}")
            return None

    def write_multiple_register(self, address, value, slave):
        try:
            if self.connected and slave > 0:
                response = self.client.write_registers(address, value, slave=slave)
                print(f"Write {len(value)} values on registers {address} to slave {slave} success")
                return 1
            return 0
        except ModbusException as e:
            # print(f'Error writing multiple registers {address} with value {value} to slave {slave}')
            print(f"Error de Modbus al escribir registros: {e}")
            return 0
        except Exception as e:
            print(f"Error inesperado al escribir registros: {e}")
            return 0

    def write_coil(self, adress, value, slave):
        try: 
            if self.connected and slave > 0:
                response = self.client.write_coil(adress, value, slave=slave)
                return 1
            return 0
        except ModbusException as e:
            print(f"Error de Modbus al escribir coil: {e}")
            return 0
        except Exception as e:
            print(f"Error inesperado al escribir coil: {e}")
            return 0

    def read_input_registers(self, address, slave, count=1):
            try:
                if self.connected and slave > 0:
                    response = self.client.read_input_registers(address, count=count, slave=slave)
                    # print(f"Read input registers {address} on slave {slave} success")
                    return response.registers
                return None
            except ModbusException as e:
                # print(f'Reading register {address} from slave {slave} failed')
                # print(f"Modbus error: {e}")
                print(f"Error de Modbus al leer input registers: {e}")
                return None
            except Exception as e:
                print(f"Error inesperado al leer input registers: {e}")
                return None

    '''
    Cada peso leido desde un dispositivo tiene la forma de:
    Peso = [Pesos a leer, id del paquete, peso inicial, peso final, tamaño del registro de pesos]
    '''

    def read_weights_from_scale(self, scale: Scale) -> list[list[int]]:
        weights = []
        weight = []
        response = [0]
        
        if self.connected and scale.slave_address > 0:
            try:
                open_read_weights_comunication = self.write_coil(0, True, scale.slave_address)
                available_registers = self.read_input_registers(0, scale.slave_address)[0]
                response = self.read_input_registers(0, scale.slave_address, available_registers * 5)#Aqui recibo un arreglo unidimensional con todos los pesos sin separar
                close_read_weights_comunication = self.write_coil(1, True, scale.slave_address)
                if open_read_weights_comunication == 1 and close_read_weights_comunication == 1 and response != None and available_registers != None:
                    print(f"Read weights from scale {scale.scale_id} with address {scale.slave_address} success")
                else:
                    print(f'open_read_weights_comunication: {open_read_weights_comunication}, close_read_weights_comunication: {close_read_weights_comunication}, response: {response}, available_registers: {available_registers}')
                    raise Exception("Error reading registers or coils")
            except ModbusException as e:
                response = [0]
                print(f"Error de Modbus leyendo pesos de scale {scale.scale_id} con address {scale.slave_address}: {e}")
                return None
            except Exception as e:
                response = [0]
                print(f"Error reading weights from scale {scale.scale_id} with address {scale.slave_address}: {e}")
                return None
        # print(f"Response from scale {slave}: {response}")
        if response != [0]:
            weights_sliced = [response[i:i+5] for i in range(0, len(response), 5)]
            weights = []
            for sub in weights_sliced[:response[0]]:
                pkg_id = int(sub[1])
                initial = sub[2] / 100.0
                final = sub[3] / 100.0
                weights.append([pkg_id, initial, final])

            weights.insert(0, scale.scale_id)
        # for i in range(response[0]): #De forma que dentro del rango de pesos a leer
        #     if (i % 5 == 0 and i != 0): #Voy juntando los registros de cada peso
        #         weights.append(weight[1:-1]) #Agrego solo paquete id, peso inicial y peso final a la lista de pesos
        #         weight = []
        #         weight.append(response[i])
        #     else:
        #         weight.append(response[i])
        # print(f"Weights from scale {scale.scale_id}: {weights}")
        return weights #De forma que weights tiene la forma de [[id del paquete, peso inicial, peso final]]

    def update_packages_for_scale(self, packages: list[Package], slave_address):
        packages_to_write = []
        if self.connected and slave_address > 0:
            try:
                for i in range(len(packages)):
                    packages_to_write.extend([len(packages), packages[i].package_id, int(packages[i].minimum_weight * 100), int(packages[i].maximum_weight * 100), 0])    
                write_packages = self.write_multiple_register(0, packages_to_write, slave_address)
                request_read_packages = self.write_coil(2, True, slave_address)
                if write_packages == 1 and request_read_packages == 1:
                    print(f"Update packages for scale address {slave_address} success")
                else:
                    raise Exception("Error writing registers or coils")
            except ModbusException as e:
                print(f"Error de Modbus actualizando paquetes para scale address {slave_address}: {e}")
            except Exception as e:
                print(f"Error updating packages for scale address {slave_address}: {e}")

    def update_package(self, package: Package):
        if self.connected:
            try:
                print("actualizando paquete")
                scales = scale.read_all()
                for scale_ in scales:
                    if any(package.package_id == p.package_id for p in scale_.packages):
                        print("coincidencia")
                        packages = scale_.packages
                        for package_ in scale_.packages:
                            if package_.package_id == package.package_id:
                                packages.remove(package_)
                                packages.append(package)
                        self.update_packages_for_scale(packages, scale_.slave_address)
                print("paquete actualizado")
            except ModbusException as e:
                print(f"Error de Modbus actualizando paquete {package.package_id}: {e}")
            except Exception as e:
                print(f"Error inesperado actualizando paquete {package.package_id}: {e}")

    def read_device_info(self, slave):
        return self.client.read_device_information(slave=slave)
    
    
    def load_packages(self, slave_address, packages):
        packages_to_write = []
        for package in packages:
            packages_to_write.extend([len(packages), package.package_id, int(package.minimum_weight * 100), int(package.maximum_weight * 100), 0])
        if self.connected:
            try:
                write_packages = self.write_multiple_register(0, packages_to_write, slave_address)
                request_read_packages = self.write_coil(2, True, slave_address)
                if write_packages == 1 and request_read_packages == 1:
                    print(f"Load packages to scale address {slave_address} success")
                else:
                    raise Exception("Error writing registers or coils")
            except ModbusException as e:
                print(f"Error de Modbus cargando paquetes en scale address {slave_address}: {e}")
            except Exception as e:
                print(f"Error loading packages to scale addres {slave_address}: {e}")


    
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(ModbusMaster, cls).__new__(cls)
        return cls._instance
    
Master = None
try:
    Master = ModbusMaster(port="COM11", baudrate=115200)
except:
    pass
