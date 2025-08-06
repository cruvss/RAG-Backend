import os

# Load environment vairables
from dotenv import load_dotenv
load_dotenv()

# Configuration constants

ALLOWED_EXTENSIONS = {'pdf', 'txt'}
MAX_FILE_SIZE = 25 * 1024 * 1024  # 25 MB
COLLECTION_NAME = "rag_documents"
DB_PATH = "app/metadata.db"
UPLOAD_DIR = "app/uploads"

# Redis Config
REDIS_CONFIG = {
    "host": "redis-17976.crce179.ap-south-1-1.ec2.redns.redis-cloud.com",
    "port": 17976,
    "decode_responses": True,
    "username": "default",
    "password": os.getenv('REDIS_PASSWORD')
}


# Email Service
SMTP_HOST = "smtp.mailersend.net"
SMTP_PORT = 587
SMTP_USER = "MS_Oi2rdx@test-2p0347zxewylzdrn.mlsender.net"
SMTP_PASS = os.getenv('SMTP_PASS')