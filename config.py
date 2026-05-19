import os
from dotenv import load_dotenv

load_dotenv()

# Gemini AI
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

# Email Settings
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
SMTP_USERNAME = os.getenv("SMTP_USERNAME", "")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
TARGET_EMAIL = "davidekins@gmail.com"

# Execution Mode
DRY_RUN = os.getenv("DRY_RUN", "True").lower() in ("true", "1", "yes")

# Database
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///agent.db")
