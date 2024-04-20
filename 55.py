import psutil
import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def get_process_memory_usage(process_name):
    try:
        process_id = None
        for proc in psutil.process_iter(['pid', 'name']):
            if proc.info['name'] == process_name:
                process_id = proc.info['pid']
                break

        if process_id is None:
            return None

        process = psutil.Process(process_id)
        memory_info = process.memory_info()
        memory_usage_mb = memory_info.rss / (1024 * 1024)  # Convert bytes to megabytes
        return memory_usage_mb
    except psutil.NoSuchProcess:
        return None

def get_process_cpu_usage(process_name):
    try:
        process_id = None
        for proc in psutil.process_iter(['pid', 'name']):
            if proc.info['name'] == process_name:
                process_id = proc.info['pid']
                break

        if process_id is None:
            return None

        process = psutil.Process(process_id)
        cpu_percent = process.cpu_percent(interval=1)  # CPU usage in percent
        return cpu_percent
    except psutil.NoSuchProcess:
        return None

def get_process_info():
    global update_flag
    process_name = entry.get()
    if process_name.strip():  # Check if the entry is not empty
        memory_usage = get_process_memory_usage(process_name)
        cpu_usage = get_process_cpu_usage(process_name)
        if memory_usage is not None and cpu_usage is not None:
            memory_data.append(memory_usage)
            cpu_data.append(cpu_usage)
            ax[0].plot(memory_data, 'r-')
            ax[1].plot(cpu_data, 'b-')
            canvas.draw()
            result_label.config(text=f"Dastur xotiradagi joy: {memory_usage:.2f} MB\nDastur CPU ishlatilishi: {cpu_usage:.2f}%")
        else:
            result_label.config(text="Xatolik: Kiritilgan dastur nomi bo'yicha topa olmadim!")
    update_flag = True

def stop_update():
    global update_flag
    update_flag = False

def update_plot():
    global update_flag
    if update_flag:
        process_name = entry.get()
        if process_name.strip():  # Check if the entry is not empty
            memory_usage = get_process_memory_usage(process_name)
            cpu_usage = get_process_cpu_usage(process_name)
            if memory_usage is not None and cpu_usage is not None:
                memory_data.append(memory_usage)
                cpu_data.append(cpu_usage)
                ax[0].plot(memory_data, 'r-')
                ax[1].plot(cpu_data, 'b-')
                canvas.draw()
                result_label.config(text=f"Dastur xotiradagi joy: {memory_usage:.2f} MB\nDastur CPU ishlatilishi: {cpu_usage:.2f}%")
            else:
                result_label.config(text="Xatolik: Kiritilgan dastur nomi bo'yicha topa olmadim!")
    root.after(1000, update_plot)

root = tk.Tk()
root.title("Dastur ma'lumotlarini olish")

label = tk.Label(root, text="Ishlatmoqchi bo'lgan dasturning nomini kiriting:")
label.pack()

entry = tk.Entry(root)
entry.pack()

button_get_info = tk.Button(root, text="Ma'lumotlarni olish", command=get_process_info)
button_get_info.pack()

button_stop_update = tk.Button(root, text="To'xtatish", command=stop_update)
button_stop_update.pack()

result_label = tk.Label(root, text="")
result_label.pack()

# Creating plots
fig, ax = plt.subplots(2, 1)
ax[0].set_title('Xotiradagi Joy (MB)')
ax[1].set_title('CPU Ishlatilishi')

memory_data = []
cpu_data = []

canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack()

update_flag = True
update_plot()
root.mainloop()