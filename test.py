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

Master = ModbusMaster(port="COM7", baudrate=115200)
Master.connect()

print(f'Result: {Master.read_input_registers(0, 4)}')
print(f'find scales: {find_scales()}')

Master.close()