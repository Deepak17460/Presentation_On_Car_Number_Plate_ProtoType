import psutil

cpu_percent = psutil.cpu_percent(interval=1)
memory_info = psutil.virtual_memory()

print(f'CPU Usage: {cpu_percent}%')
print(f'Memory Usage: {memory_info.percent}%')