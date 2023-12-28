from datetime import datetime
import time
import sqlite3
from w1thermsensor import W1ThermSensor#模块在https://pypi.org/project/w1thermsensor/

#获取ds18b20的温度值，将温度值每隔30秒插入到数据库temp_ds.dbo中
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
    total_runtime_hours = 72
    total_runtime_seconds = total_runtime_hours * 60 * 60

    # 设置每次运行间隔为 5 秒
    interval_seconds = 30


    
    while True:
        temperature = read_temperature()
        query = "INSERT INTO temp_list (temp) VALUES (?); "
        mycur.execute(query, (temperature,))
        mydb.commit()
        # 获取当前时间
        current_time = datetime.now()

        # 将时间对象格式化为字符串
        formatted_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
        print(f"当前温度: {temperature:.2f} 摄氏度 "+formatted_time)
        time.sleep(interval_seconds)
    
