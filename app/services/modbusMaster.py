from pymodbus.client.sync import ModbusSerialClient
from pymodbus.exceptions import ModbusException

class ModbusMaster:
    def __init__(self, port, baudrate=9600, timeout=1):
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.client = ModbusSerialClient(method='rtu', port=port, baudrate=baudrate, timeout=timeout)

    def connect(self):
        if not self.client.connect():
            raise ModbusException("Unable to connect to Modbus server")

    def close(self):
        self.client.close()

    def read_registers(self, address, count, unit=1):
        try:
            response = self.client.read_holding_registers(address, count, unit=unit)
            if response.isError():
                raise ModbusException("Error reading registers")
            return response.registers
        except ModbusException as e:
            print(f"Modbus error: {e}")
            return None

    def write_register(self, address, value, unit=1):
        try:
            response = self.client.write_register(address, value, unit=unit)
            if response.isError():
                raise ModbusException("Error writing register")
            return response
        except ModbusException as e:
            print(f"Modbus error: {e}")
            return None