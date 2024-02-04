from pymodbus.client import ModbusSerialClient
import time
# 串口参数
serial_port = '/dev/ttyUSB0'

# 创建 Modbus RTU 串口客户端
client = ModbusSerialClient(port=serial_port,baudrate= 9600,timeout=0.5)
client.connect()
i=0
# 循环读取温度值

# 读取温度寄存器值
temperature_register = client.read_holding_registers(0, 8, 1)
temperature = temperature_register.registers


# 判断读取是否成功
if temperature_register.registers:
    # 遍历读取到的寄存器值
    for value in temperature_register.registers:
        # 将读取到的值转换为温度值
        if value > 32767:
            value = value - 65536  # 进行符号位扩展
        temperature = value / 10
        i += 1

        # 打印温度值
        print(str(i) + f'    温度：{temperature}℃')
else:
    print('读取温度值失败')

# 关闭串口连接
client.close()