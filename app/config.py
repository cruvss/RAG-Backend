"""Application configuration loaded from environment variables and defaults."""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# File handling
ALLOWED_EXTENSIONS: set[str] = {"pdf", "txt"}
MAX_FILE_SIZE: int = 25 * 1024 * 1024  # 25 MB
COLLECTION_NAMES: tuple[str, ...] = ("semantic", "recursive")
DB_PATH: Path = Path("app/metadata.db")
UPLOAD_DIR: Path = Path("app/uploads")

# Redis configuration
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD")
if not REDIS_PASSWORD:
    raise RuntimeError("Missing required environment variable: REDIS_PASSWORD")

REDIS_CONFIG: dict[str, object] = {
    "host": "redis-17976.crce179.ap-south-1-1.ec2.redns.redis-cloud.com",
    "port": 17976,
    "decode_responses": True,
    "username": "default",
    "password": REDIS_PASSWORD,
}

# Email service
SMTP_PASS = os.getenv("SMTP_PASS")
if not SMTP_PASS:
    raise RuntimeError("Missing required environment variable: SMTP_PASS")

SMTP_HOST: str = "smtp.mailersend.net"
SMTP_PORT: int = 587
SMTP_USER: str = "MS_Oi2rdx@test-2p0347zxewylzdrn.mlsender.net"
