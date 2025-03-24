import time
import psutil
import logging
import win32event
import win32con
import win32api

# Set up logging
logging.basicConfig(filename="system_monitor_log.txt", level=logging.INFO, format="%(asctime)s - %(message)s")

def get_system_uptime():
    return win32api.GetTickCount() // 1000  # Convert ms to seconds

def get_cpu_usage():
    return psutil.cpu_percent(interval=1)

def get_process_usage(pid):
    try:
        process = psutil.Process(pid)
        cpu_usage = process.cpu_percent(interval=1)
        memory_info = process.memory_info().rss / (1024 * 1024)  # Convert bytes to MB
        return cpu_usage, memory_info
    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
        return None, None

def get_running_processes():
    processes = []
    for process in psutil.process_iter(attrs=['pid', 'name']):
        try:
            processes.append((process.info['pid'], process.info['name']))
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return processes

def monitor_system():
    try:
        threshold_cpu = float(input("Enter CPU usage threshold in %: "))
        threshold_memory = float(input("Enter memory usage threshold in MB: "))
    except ValueError:
        print("Invalid input for thresholds. Please enter numeric values.")
        return    
    
    print(f"System uptime: {get_system_uptime()} seconds")
    print("Monitoring system performance... Press Ctrl+C to end the program.")
    
    while True:
        try:
            total_cpu_usage = get_cpu_usage()
            print(f"Total CPU Usage: {total_cpu_usage}%")
            logging.info(f"Total CPU Usage: {total_cpu_usage}%")
            
            running_processes = get_running_processes()
            for pid, name in running_processes:
                cpu_usage, memory_usage = get_process_usage(pid)
                if cpu_usage is not None and memory_usage is not None:
                    if cpu_usage > threshold_cpu or memory_usage > threshold_memory:
                        print(f"High Resource Usage: {name} (PID: {pid}) - CPU: {cpu_usage}%, Memory: {memory_usage} MB")
                        logging.info(f"High Resource Usage: {name} (PID: {pid}) - CPU: {cpu_usage}%, Memory: {memory_usage} MB")
            
            event = win32event.CreateEvent(None, 0, 0, "SystemMonitorEvent")
            win32event.SetEvent(event)
            time.sleep(2)

        except KeyboardInterrupt:
            print("Monitoring stopped.")
            logging.info("Monitoring stopped by user.")
            break

if __name__ == "__main__":
    monitor_system()
