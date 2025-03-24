""" 
System Monitoring Script for Windows

This script will monitor system performance, including CPU usage, memory usage,
and running processes. Allows users to set custom thresholds for CPU and memory usage 
and logs any high resource detected.

CPRG-217-A March 23, 2025
Group 8
Clayton Ma 760796, Allen Amil 959926, Muhammad Khan 957149, Dustin Nguyen 737507, Xiangzhi Gu 538190
"""


import time
import psutil
import win32api
import win32process
import win32pdh
import win32event
import win32con
import logging
import os

print("Current Working Directory:", os.getcwd())

# Set up logging to write results to a file
try:
    logging.basicConfig(filename="system_monitor_log.txt", level=logging.INFO, format="%(asctime)s - %(message)s")
except Exception as e:
    print(f"Error setting up logging: {e}")



# Function to get system uptime using win32api
def get_system_uptime():
    return win32api.GetTickCount() // 1000  # Convert ms to seconds



# Function to get CPU usage using win32pdh
def get_cpu_usage():
    try:
        hQuery = win32pdh.OpenQuery()
        hCounter = win32pdh.AddCounter(hQuery, "\Processor(_Total)\% Processor Time")
        win32pdh.CollectQueryData(hQuery)
        time.sleep(1)  # Allow time for data collection
        win32pdh.CollectQueryData(hQuery)
        _, value = win32pdh.GetFormattedCounterValue(hCounter, win32pdh.PDH_FMT_LONG)
        win32pdh.CloseQuery(hQuery)
        return value
    except Exception as e:
        logging.error(f"Error while querying CPU usage: {str(e)}")
        return None



# Function to get process CPU and memory usage
def get_process_usage(pid):
    try:
        process = psutil.Process(pid)
        cpu_usage = process.cpu_percent(interval=1)
        memory_info = process.memory_info().rss / (1024 * 1024)  # Convert bytes to MB
        return cpu_usage, memory_info
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        return None, None



# def get_process_usage(pid):
def get_running_processes():
    try:
        process_ids = win32process.EnumProcesses()
        processes = []
        for pid in process_ids:
            try:
                handle = win32api.OpenProcess(win32con.PROCESS_QUERY_INFORMATION | win32con.PROCESS_VM_READ, False, pid)
                module_name = win32process.GetModuleFileNameEx(handle, 0)
                processes.append((pid, module_name))
                win32api.CloseHandle(handle)
            except Exception as e:
                logging.error(f"Could not retrieve information for process PID {pid}: {str(e)}")
                continue
        return processes
    except Exception as e:
        logging.error(f"Error enumerating processes: {str(e)}")
        return []    



# Function to monitor system stats with user-defined thresholds
def monitor_system(threshold_cpu=50, threshold_memory=200):
    try:
        threshold_cpu = float(input("Enter CPU usage threshold in %: "))  # User input for CPU threshold
        threshold_memory = float(input("Enter memory usage threshold in MB: "))  # User input for memory threshold
    except ValueError:
        print("Invalid input for thresholds. Please enter numeric values.")
        return    
    
    print(f"System uptime: {get_system_uptime()} seconds")
    print("Monitoring system performance... Press Ctrl+C to end the program.")
    
    while True:
        try:
            total_cpu_usage = get_cpu_usage()
            if total_cpu_usage is not None:
                print(f"Total CPU Usage: {total_cpu_usage}%")
                logging.info(f"Total CPU Usage: {total_cpu_usage}%")
            
            running_processes = get_running_processes()
            for pid, name in running_processes:
                cpu_usage, memory_usage = get_process_usage(pid)
                if cpu_usage is not None and memory_usage is not None:
                    if cpu_usage > threshold_cpu or memory_usage > threshold_memory:
                        print(f"High Resource Usage: {name} (PID: {pid}) - CPU: {cpu_usage}%, Memory: {memory_usage} MB")
                        logging.info(f"High Resource Usage: {name} (PID: {pid}) - CPU: {cpu_usage}%, Memory: {memory_usage} MB")
            
            # Simulate an event trigger using win32event
            event = win32event.CreateEvent(None, 0, 0, "SystemMonitorEvent")
            win32event.SetEvent(event)

            time.sleep(2)

        except KeyboardInterrupt:
            print("Monitoring stopped.")
            logging.info("Monitoring stopped by user.")
            break



if __name__ == "__main__":
    monitor_system()
