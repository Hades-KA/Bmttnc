import psutil
import platform
import socket
import logging
import time

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    filename="system_monitor.log",
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger()


# Hàm sẽ ghi thông tin vào file log và in ra màn hình
def log_info(category, message):
    logger.info(f"{category}: {message}")
    print(f"{category}: {message}")


# Giám sát CPU và Bộ nhớ
def monitor_cpu_memory():
    cpu_percent = psutil.cpu_percent()
    memory_info = psutil.virtual_memory()
    log_info("CPU", f"Usage: {cpu_percent}%")
    log_info("Memory", f"Usage: {memory_info.percent}%")


# Giám sát thông tin hệ thống
def monitor_system_info():
    os_info = platform.uname()
    hostname = socket.gethostname()
    log_info("System Info", f"Hostname: {hostname}")
    log_info("System Info", f"Operating System: {os_info.system} {os_info.release}")
    log_info("System Info", f"Python Version: {platform.python_version()}")


# Giám sát trạng thái mạng
def monitor_network():
    net_stats = psutil.net_io_counters()
    log_info(
        "Network",
        f"Bytes Sent: {net_stats.bytes_sent}, Bytes Received: {net_stats.bytes_recv}",
    )


# Giám sát danh sách phần mềm đang chạy
def monitor_software():
    software_list = psutil.process_iter(attrs=["pid", "name", "username"])
    log_info("Software", "Running Software:")
    for software in software_list:
        software_name = software.info["name"]
        software_pid = software.info["pid"]
        software_username = software.info["username"]
        log_info(
            "Software",
            f"PID: {software_pid}, Name: {software_name}, Username: {software_username}",
        )


# Giám sát hệ thống toàn diện
def monitor_system():
    log_info("System Monitor", "Starting system monitoring...")
    while True:
        monitor_cpu_memory()
        monitor_system_info()
        monitor_network()
        monitor_software()
        log_info("System Monitor", "------------------------------------")
        time.sleep(60)


if __name__ == "__main__":
    monitor_system()
