import asyncio
import struct
import time
from sqlalchemy import text
from pymodbus.exceptions import ModbusException
import numpy as np
from app.db.base import Base, Meta, conn, engine, session
from app.models.scale import Scale
from app.models.weight import Weight
from app.models.package import Package
from app.models.scales_has_packages import ScaleHasPackages
from app.crud import scale
import pandas as pd
from app.services.modbusMaster import ModbusMaster
from datetime import datetime
from app.services.scales import find_scales
import serial

# Master = ModbusMaster("COM10", 19200)
# Master.connect()
# # Master.read_device_info(1)
#
# print(f'Result: {Master.read_input_registers(0, 3)}')
# print(f'find scales: {find_scales()}')

PORT = "COM10"   # o COMx en Windows
BAUD = 19200

def connnectSerial(port, baud, timeout=0.2):
    try:
        ser = serial.Serial(port, baudrate=baud, timeout=timeout)
        print(f"Conectado a {port} a {baud} baudios")
        return ser
    except serial.SerialException as e:
        print(f"Error al conectar: {e}")
        return None

def readSerial(ser):
    print("Leyendo datos...")
    try:
        while True:
            line = ser.readline()
            if line:
                try:
                    print(line.decode().strip())
                except UnicodeDecodeError:
                    print("⚠️ Dato corrupto:", line)
    except KeyboardInterrupt:
        print("Saliendo")
    finally:
        ser.close()

def writeSerial(ser):
    counter = 0
    try:
        while True:
            msg = f"PY,{counter},{int(time.time()*1000)}\n"
            ser.write(msg.encode())
            ser.flush()
            print("→ enviado:", msg.strip())
            counter += 1
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("Saliendo")
    finally:
        ser.close()

try:
    ser = connnectSerial(PORT, BAUD)
    if ser:
        readSerial(ser)  # Solo lectura
        # writeSerial(ser)  # Solo escritura
except Exception as e:
    print(f"Error: {e}")