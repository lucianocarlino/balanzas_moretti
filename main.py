import serial

com = serial.Serial('COM4', 9600, timeout=5, parity=serial.PARITY_EVEN, stopbits=serial.STOPBITS_TWO, bytesize=serial.SEVENBITS)

while True:
    
    linea = com.readline(18)

    print(f'valor leido {linea}')

