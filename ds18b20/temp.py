import time
import sqlite3
from w1thermsensor import W1ThermSensor#模块在https://pypi.org/project/w1thermsensor/
def read_temperature():
    # 获取 DS18B20 传感器列表
    sensors = W1ThermSensor.get_available_sensors()
    
    if sensors:
        # 获取第一个传感器的温度
        temperature_in_celsius = sensors[0].get_temperature()
        return temperature_in_celsius
    else:
        print("未找到 DS18B20 传感器")
if __name__ == "__main__":
    # 设置 GPIO 编号
    # W1ThermSensor.set_default_gpio(17)  # 使用 GPIO17
    mydb=sqlite3.connect('temp_ds.db')
   
    mycur = mydb.cursor()
    total_runtime_hours = 24
    total_runtime_seconds = total_runtime_hours * 60 * 60

    # 设置每次运行间隔为 5 秒
    interval_seconds = 30

    # 获取程序开始时间
    start_time = time.time()
    
    while time.time() - start_time < total_runtime_seconds:
        temperature = read_temperature()
        query = "INSERT INTO temp_list (temp) VALUES (?); "
        mycur.execute(query, (temperature,))
        mydb.commit()
        time.sleep(interval_seconds)
    
