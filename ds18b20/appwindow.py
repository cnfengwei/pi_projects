import tkinter as tk
from tkinter import ttk
from sqlite3 import connect
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.font_manager import FontProperties
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta
import socket
def plot_temperature_data(data):

    # 创建图形和轴
    fig, ax = plt.subplots()

    # 绘制数据
    temp_y = [item[1] for item in data]
    date_x = [datetime.strptime(item[2], '%Y-%m-%d %H:%M:%S') for item in data]
    ax.plot(date_x, temp_y)

    # 设置 x 轴的时间刻度
    hours = mdates.HourLocator(interval=1)  # 设置每小时一个刻度
    ax.xaxis.set_major_locator(hours)

    # 设置 x 轴的时间刻度格式
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H'))

    # 设置 x 轴的范围
    ax.set_xlim(date_x[0], date_x[0] + timedelta(hours=24))
    ax.set_ylim(-40, 60)
    ax.set_yticks(range(-40, 61, 10))
    ax.set_yticklabels([str(deg) + '°' for deg in range(-40, 61, 10)])

    # 设置 x 轴标签
    plt.title('温度曲线图', fontproperties=font)
    ax.set_xlabel('日期',fontproperties=font)

    # 设置 y 轴标签
    ax.set_ylabel('温度',fontproperties=font)
    ax.grid(True)
   
    return fig


# 获取当前脚本所在目录
font = FontProperties(fname=r'NotoSerifCJKsc-Light.ttf', size=12)





# 创建主窗口
window = tk.Tk()
window.title('温度记录')

window.geometry('800x600+500+200')
# 创建 Frame
button_frame = tk.Frame(window,bg="#4C2A85")

main_frame=tk.Frame(window,bg='blue')

button_frame.pack(side="left", fill="y")
main_frame.pack(fill='both', expand=True)
curtemp_btn=ttk.Button(button_frame,text='当前温度')
curtemp_btn.grid(row=0)
templist_btn = ttk.Button(button_frame,text='welist')
templist_btn.grid(row=1)



# # 连接数据库
with connect('temp_ds.db') as myconn:
    mycur = myconn.cursor()
    query = "SELECT * FROM temp_list "#WHERE date >= '2023-12-15 00:00:00' AND date < '2023-12-16 00:00:00'" 
    mycur.execute(query)
    data = mycur.fetchall()
mycur.close()
myconn.close()
#绘制图形
fig = plot_temperature_data(data)

# 将 Matplotlib 图形嵌入到 Tkinter 窗口中
canvas = FigureCanvasTkAgg(fig, master=main_frame)
canvas.draw()
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

# 创建一个TCP/IP套接字
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 连接服务器的地址和端口
server_address = ('10.0.0.16', 12345)
client_socket.connect(server_address)

try:
    while True:
        # 接收数据并解码
        data = client_socket.recv(1024).decode('utf-8')

        # 处理温度数据
        temperature = float(data)
        print('当前温度：', temperature)

except KeyboardInterrupt:
    pass
finally:
    # 清理连接
    client_socket.close()



# 运行 Tkinter 主循环
window.mainloop()










