import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:

    SECRET_KEY = "talentai-secret-key"

    DATABASE = os.path.join(BASE_DIR, "database.db")

    UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")

    REPORT_FOLDER = os.path.join(BASE_DIR, "reports")

    MAX_CONTENT_LENGTH = 16 * 1024 * 1024

    ALLOWED_EXTENSIONS = {"pdf", "docx"}