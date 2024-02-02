from pymodbus.client import ModbusSerialClient
from pymodbus import Framer
baud_rate = 9600
serial_port = 'COM7'

client = ModbusSerialClient(
    
    framer = Framer.RTU,
    port=serial_port,
    baudrate=baud_rate,
    stopbits=1,
    bytesize=8,
    parity='N',  # 无校验
    timeout=1
)

try:
    client.connect()
    rr = client.read_holding_registers(1, 1, 1)
    response = rr.registers
    print(response)
except Exception as e:
    print(f"Modbus communication error: {e}")
finally:
    client.close()
