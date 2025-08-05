# Load environment vairables
from dotenv import load_dotenv

load_dotenv()


# Configuration constants

ALLOWED_EXTENSIONS = {'pdf', 'txt'}
MAX_FILE_SIZE = 25 * 1024 * 1024  # 25 MB
COLLECTION_NAME = "rag_documents"
DB_PATH = "app/metadata.db"
UPLOAD_DIR = "app/uploads"
