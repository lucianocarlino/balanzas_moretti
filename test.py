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

Master = ModbusMaster(port="COM7", baudrate=115200)
Master.connect()

registros = []
start_time = time.time()

def main():
    try:
        # Escritura de datos para la modificacion de envases
        """
        await Master.write_register(0, 15, 2)
        await Master.write_register(1, 45.36, 2)
        await Master.write_register(2, 100.85, 2)
        await Master.write_coil(0, True, 2)
        """
        # Lectura de datos de pesaje
        Master.write_coil(2, True, 3)
        Master.write_coil(0, True, 2)
        print(f'Tiempo start_reading: {time.time() - start_time} segundos')
        available_registers = Master.read_input_registers(0, 2)
        print(f'Tiempo available_registers: {time.time() - start_time} segundos')
        print(f'Available registers: {available_registers}')
        print(f'Read {(available_registers[0]) * 5} registers')
        if available_registers[0] > 0:
            consulta = Master.read_input_registers(0, 2, (available_registers[0]) * 5)
            # for i in range(available_registers):
            #     envase_id = Master.read_input_registers(1 + (5 * i), 2)
            #     initial_weight = Master.read_input_registers(2 + (5 * i), 2)
            #     final_weight = Master.read_input_registers(3 + (5 * i), 2)
            #     registros.append((envase_id, initial_weight, final_weight))
            print(f'Tiempo registers_read: {time.time() - start_time} segundos')
        else:
            consulta = []
        Master.write_coil(1, True, 2)
        print(f'Tiempo finish_reading: {time.time() - start_time} segundos')
        registros.append(consulta)
        # print(f'Peso inicial: {initial_weight}, Peso final: {final_weight}')



    except ModbusException as e:
        print(f"Error: {e}")

# while True:
# main()

def conectar_db():
    # print("Conectando a la base de datos")
    #Escritura en db

    # Base.metadata.create_all(engine)

    # test_package_1 = Package(name="package_test_1", expected_weight = -1, minimum_weight = -1.5, maximum_weight = -0.5, scales=[])
    # test_scale_1 = Scale(name="scale_test_1", packages=[test_package_1], mapped=True, online=False)
    # test_package_2 = Package(name="test_2", expected_weight = 100, minimum_weight = 95, maximum_weight = 105, scales=[])
    # test_scale_2 = Scale(name="scale_test_2", packages=[test_package_2], mapped=True, online=True)

    # session.add_all([test_scale_2, test_scale_1, test_package_2, test_package_1])
    # session.commit()

    # result = session.query(Scale).all()
    # print(type(result))
    # print(result)
    package_1 = session.query(Package).filter(Package.package_id == 1).first()
    package_2 = session.query(Package).filter(Package.package_id == 2).first()
    scale_1 = session.query(Scale).filter(Scale.scale_id == 1).first()
    scale_2 = session.query(Scale).filter(Scale.scale_id == 2).first()

    test_weight_1 = Weight(date_time=datetime.date(0), initial_weight=0.5, final_weight=1.5, package=package_1, scale=scale_1)
    test_weight_2 = Weight(date_time=datetime.date(0), initial_weight=0.5, final_weight=1.5, package=package_1, scale=scale_2)
    test_weight_3 = Weight(date_time=datetime.date(0), initial_weight=0.5, final_weight=1.5, package=package_2, scale=scale_1)
    test_weight_4 = Weight(date_time=datetime.date(0), initial_weight=0.5, final_weight=1.5, package=package_2, scale=scale_2)

    session.add_all([test_weight_1, test_weight_2, test_weight_3, test_weight_4])
    session.commit()

    # scale = session.query(Scale).filter(Scale.scale_id == 2).first()
    # package = scale.packages[0]
    # print(package.package_id)

    #Lectura de todos los registros de la db
    '''
    result = conn.execute(Scale.__table__.select()).fetchall()
    '''
    #Lectura de un registro de la db
    '''
    result = conn.execute(Scale.__table__.select().where(Scale.scale_id == 4)).fetchone()
    '''
    #Actualizacion de un registro de la db
    '''
    conn.execute(Scale.__table__.update().where(Scale.scale_id == 4).values(slave_address=10))
    conn.commit()
    result = conn.execute(Scale.__table__.select().where(Scale.scale_id == 4)).fetchone()
    '''
    #Eliminacion de un registro de la db
    '''
    conn.execute(Scale.__table__.delete().where(Scale.scale_id == 0))
    conn.commit()
    result = conn.execute(Scale.__table__.select().where(Scale.scale_id == 0)).fetchone()
    '''

# Base.metadata.drop_all(engine)
# Base.metadata.create_all(engine)    
conectar_db()


end_time = time.time()
elapsed_time = end_time - start_time
print(f'Tiempo de ejecucion: {elapsed_time} segundos')
print(f'Lecturas realizadas: {registros}')

# print(tiempos)
# print(f'El mayor tiempo fue de {max(tiempos)}')
# print(f'El menor tiempo fue de {min(tiempos)}')
# print(f'El tiempo promedio fue de {sum([i[0] for i in tiempos])/len(tiempos)}')
# print(f'Hubo {len([i for i in tiempos if i[1] == True])} de {len(tiempos)} veces que se cumplieron las condiciones')
# print(f'Las veces que ocurrio un error fueron {[i for i in tiempos if i[1] == False]}')

# weights = [[21, 15, 365, 730, 0, 0, 15, 365, 730, 0, 0, 15, 365, 730, 0, 0, 15, 365, 730, 0, 0, 15, 365, 730, 0, 0, 15, 365, 730, 0, 0, 15, 365, 730, 0, 0, 15, 365, 730, 0, 0, 15, 365, 730, 0, 0, 15, 365, 730, 0, 0, 15, 365, 730, 0, 0, 15, 365, 730, 0, 0, 15, 365, 730, 0, 0, 15, 365, 730, 0, 0, 15, 365, 730, 0, 0, 15, 365,
# 730, 0, 0, 15, 365, 730, 0, 0, 15, 365, 730, 0, 0, 15, 365, 730, 0, 0, 15, 365, 730, 0, 0, 15, 365, 730, 0]]

# weight = []

# weights_modified = []

# print(len(registros[0]))

# for i in range(len(registros[0])):
#     if (i % 5 == 0 and i != 0):
#         weights_modified.append(weight[1:-1])
#         weight = []
#         weight.append(registros[0][i])
#     else:
#         weight.append(registros[0][i])
# print(weights_modified)

def generate_csv(weights):
    weights_data = [weight.to_dict() for weight in weights]
    df = pd.DataFrame(weights_data)
    df.to_csv("weights.csv", index=False)

# generate_csv(session.query(Weight).all())
Master.close()