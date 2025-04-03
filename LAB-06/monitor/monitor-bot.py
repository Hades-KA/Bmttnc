import psutil
import logging
import time
import asyncio
from telegram import Bot

# Mã token của bot, dùng để xác thực với API Telegram
BOT_TOKEN = "7784879301:AAEfUyZJUy6qN3-91GkWfnN5teUW4tryLUI" # ĐỔI BOT_TOKEN 
# ID của chat (có thể là nhóm hoặc người dùng) nơi bạn muốn gửi thông báo
CHAT_ID = "-4619536475" # ĐỔi CHAT_ID
# Configure logging
logging.basicConfig(
    level=logging.INFO,
    filename="system_monitor_bot.log",
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger()


# Ghi thông tin vào file log và in thông điệp ra màn hình.
def log_info(category, message):
    logger.info(f"{category}: {message}")
    print(f"{category}: {message}")


# Hàm gửi tin nhắn Telegram bất đồng bộ
async def send_telegram_message(message):
    bot = Bot(token=BOT_TOKEN)
    await bot.send_message(chat_id=CHAT_ID, text=message)


# Hàm giám sát CPU và Bộ nhớ
def monitor_cpu_memory():
    cpu_percent = psutil.cpu_percent()
    memory_info = psutil.virtual_memory()
    log_info("CPU", f"Usage: {cpu_percent}%")
    log_info("Memory", f"Usage: {memory_info.percent}%")
    # Gửi thông báo qua Telegram
    message = f"CPU Usage: {cpu_percent}%\nMemory Usage: {memory_info.percent}%"
    asyncio.run(send_telegram_message(message))


# Hàm giám sát hệ thống toàn diện
def monitor_system():
    log_info("System Monitor", "Starting system monitoring...")
    while True:
        monitor_cpu_memory()
        log_info("System Monitor", "------------------------------------")
        time.sleep(60)


if __name__ == "__main__":
    monitor_system()
