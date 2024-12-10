import asyncio
import pymodbus.client as ModbusClient
from pymodbus.exceptions import ModbusException

class ModbusMaster:
    def __init__(self, port, baudrate=9600, timeout=1):
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout        
        # self.client = AsyncModbusSerialClient(schedulers.ASYNC_IO, method='rtu', port=port, baudrate=baudrate, timeout=timeout)

    async def connect(self):
        self.client = ModbusClient.AsyncModbusSerialClient(port=self.port, baudrate=self.baudrate, timeout=self.timeout)
        await self.client.connect()
        if not self.client.connect():
            raise ModbusException("Unable to connect to Modbus server")

    def close(self):
        self.client.close()

    async def read_registers(self, address, count, unit=1):
        try:
            response = await self.client.protocol.read_holding_registers(address, count, unit=unit)
            if response.isError():
                raise ModbusException("Error reading registers")
            return response.registers
        except ModbusException as e:
            print(f"Modbus error: {e}")
            return None

    async def write_register(self, address, value, unit=1):
        try:
            response = await self.client.protocol.write_register(address, value, unit=unit)
            if response.isError():
                raise ModbusException("Error writing register")
            return response
        except ModbusException as e:
            print(f"Modbus error: {e}")
            return None