from pymodbus.client import ModbusSerialClient
import logging
FORMAT = ('%(asctime)-15s %(threadName)-15s '
          '%(levelname)-8s %(module)-15s:%(lineno)-8s %(message)s')
logging.basicConfig(format=FORMAT)
log = logging.getLogger()
log.setLevel(logging.DEBUG)

from pymodbus.client import AsyncModbusSerialClient
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder

# 串口参数
serial_port = 'COM7'
baud_rate = 1200
  # 'E' 为偶校验，'O' 为奇校验，'N' 为无校验
stop_bits = 1
data_bits = 8

# 从机地址
unit_id = 8

# 创建 Modbus RTU 串口客户端
client = AsyncModbusSerialClient(
    method='rtu',
    port=serial_port,
    baudrate=baud_rate,
    stopbits=stop_bits,
    bytesize=data_bits,
    parity='O',
    timeout=1
)

# 打开串口连接
client.connect()

# 设置读数据命令的起始寄存器地址
start_register_address = 0xAB

# 读取寄存器数据
register_address = start_register_address
data_count = 10
request = client.read_holding_registers(171, data_count, unit=unit_id)
response = client.execute(request)

# 处理响应
if response.isError():
    print(f"Modbus error: {response.message}")
else:
    decoder = BinaryPayloadDecoder.fromRegisters(response.registers, endian=Endian.Big)
    decoded_data = decoder.decode_32bit_float()  # 32位浮点数解码，根据实际情况调整
    print(f"Received data: {decoded_data}")

# 关闭串口连接
client.close()