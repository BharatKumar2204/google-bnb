import os
from dotenv import load_dotenv
import logging

load_dotenv()

class Config:
    # Server
    MCP_SERVER_HOST = os.getenv("MCP_SERVER_HOST", "localhost")
    MCP_SERVER_PORT = int(os.getenv("MCP_SERVER_PORT", 8000))
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
    
    # Google Cloud
    GCP_PROJECT_ID = os.getenv("GCP_PROJECT_ID")
    GCP_REGION = os.getenv("GCP_REGION", "us-central1")
    GOOGLE_APPLICATION_CREDENTIALS = os.getenv(
        "GOOGLE_APPLICATION_CREDENTIALS",
        os.path.join(os.path.dirname(__file__), "credentials.json")
    )
    
    # Google APIs
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    GOOGLE_SEARCH_API_KEY = os.getenv("GOOGLE_SEARCH_API_KEY") or os.getenv("GEMINI_API_KEY")
    GOOGLE_SEARCH_ENGINE_ID = os.getenv("GOOGLE_SEARCH_ENGINE_ID")
    GOOGLE_FACT_CHECK_API_KEY = os.getenv("GOOGLE_FACT_CHECK_API_KEY")
    
    # News APIs
    GOOGLE_NEWS_API_KEY = os.getenv("GOOGLE_NEWS_API_KEY") or os.getenv("NEWS_API_KEY")
    NEWS_API_KEY = os.getenv("NEWS_API_KEY")
    APILAYER_API_KEY = os.getenv("APILAYER_API_KEY")
    TWITTER_BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")
    REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
    REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
    GOOGLE_FACT_CHECK_API_KEY = os.getenv("GOOGLE_FACT_CHECK_API_KEY")
    
    # Vertex AI Models
    VERTEX_MODEL_ID = os.getenv("VERTEX_MODEL_ID", "gemini-2.5-pro")
    VERTEX_VISION_MODEL = os.getenv("VERTEX_VISION_MODEL", "gemini-2.5-pro")
    VERTEX_FLASH_LITE_MODEL = os.getenv("VERTEX_FLASH_LITE_MODEL", "gemini-2.5-pro")
    
    # Database
    FIRESTORE_DATABASE = os.getenv("FIRESTORE_DATABASE", "news-app-db")
    
    # Caching
    CACHE_TTL = int(os.getenv("CACHE_TTL", 300))
    ENABLE_CACHE = os.getenv("ENABLE_CACHE", "True").lower() == "true"

def initialize_gcp_clients(config: Config) -> dict:
    """Initialize Google Cloud clients"""
    try:
        from google.cloud import aiplatform, firestore, storage
        
        if os.path.exists(config.GOOGLE_APPLICATION_CREDENTIALS):
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = config.GOOGLE_APPLICATION_CREDENTIALS
        
        aiplatform.init(project=config.GCP_PROJECT_ID, location=config.GCP_REGION)
        firestore_client = firestore.Client(project=config.GCP_PROJECT_ID)
        storage_client = storage.Client(project=config.GCP_PROJECT_ID)
        
        return {
            "aiplatform": aiplatform,
            "firestore": firestore_client,
            "storage": storage_client,
            "config": config
        }
    except Exception as e:
        logging.error(f"GCP initialization failed: {str(e)}")
        raise

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("mcp_server")
