import logging
from pathlib import Path

# Ensure logs folder exists
Path("logs").mkdir(exist_ok=True)

# Create a dedicated logger
logger = logging.getLogger("AgentLogger")
logger.setLevel(logging.DEBUG)

# File handler: all debug/info go to file
file_handler = logging.FileHandler("logs/agent.log", mode="a", encoding="utf-8")
file_handler.setLevel(logging.DEBUG)
file_formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
file_handler.setFormatter(file_formatter)
logger.addHandler(file_handler)

# Optional: Console handler only for warnings/errors
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.WARNING)
console_formatter = logging.Formatter("%(message)s")
console_handler.setFormatter(console_formatter)
logger.addHandler(console_handler)
