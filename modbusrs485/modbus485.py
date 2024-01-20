#首先安装pip install pymodbus
#pip install pyserial
#终端运行命令ls /dev/tty*，查找端口号


from pymodbus.client import ModbusSerialClient

# 设置串口参数，根据实际情况修改
serial_port = '/dev/ttyUSB0'
baud_rate = 9600

# 创建 Modbus RTU 串口客户端
client = ModbusSerialClient(
    method='rtu',
    port=serial_port,
    baudrate=baud_rate,
    stopbits=1,
    bytesize=8,
    parity='N',  # 无校验
    timeout=1
)

# 尝试连接到 Modbus RTU 设备
client.connect()



#第一个参数为读取第几个通道的数值，第二个参数为读取几个数值，第三个参数为从站地址
#（0,8，1）从第1个通道开始读取数值，读取8个寄存器的数值【20,21,22,23,24,25,26,27】
#（7,1,1）从第8通道开始读取，只读取一个数值【27】
rr = client.read_holding_registers(6,1,1)
       

# 发送 Modbus RTU 读取指令rr.bits为读取线圈，rr.registers为读取寄存器指令
response = rr.registers
#读取的数值除10,得到的是正确数值
# 如果数值为FCD4,那么就是一个有符号的整数

# 首先，将 FCD4 转换为二进制表示：1111110011010100。
# 由于最高位是1，表示这是一个负数。
# 对所有位进行取反操作得到 0000001100101011。
# 然后，将结果加1得到 0000001100101100。
# 最后，将二进制数 0000001100101100 转换为十进制，得到 -812
temperature = int(response[0]) / 10
print(temperature)

client.close()