from app.services.modbusMaster import Master
from app.crud.scale import read_all

def find_scales():
    scales = []
    Master.connect()
    if Master.connected:
        for slave in range(1, 15):
            print(f'Buscando en el slave {slave}')
            try:
                result = Master.read_input_registers(0, slave)
                print(result)
                scales.append(slave)
            except Exception as e:
                print(f"Slave {slave} not found")
                continue
    if len(scales) == 0:
        scales = [-1]
    return scales

def set_up_scales(scales):
    for scale in scales:
        print(f"Setting up scale address {scale.slave_address}")
        Master.load_packages(scale.slave_address, scale.packages)
        scale.online = True
