from flask_caching import Cache
from datetime import timedelta
from celery.schedules import crontab

class Config:
    # General Configuration
    SECRET_KEY = "your_secret_key_here"  # Replace with your own secret key
    SQLALCHEMY_DATABASE_URI = "sqlite:///iescp.db"  # SQLite Database URI
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Disable modification tracking for performance

    # Redis Cache configuration
    CACHE_TYPE = 'redis'
    CACHE_DEFAULT_TIMEOUT = 100
    CACHE_KEY_PREFIX = 'iescp_prefix'  # Custom prefix for cache keys
    CACHE_REDIS_URL = "redis://localhost:6379/1"  # Redis URL for cache (assuming Redis is running locally)
    
        # Flask-Mail configuration
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'mayank.tripathi_btech21@gsv.ac.in'
    MAIL_PASSWORD = 'wjwdwhooxzbgyulc'
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False

    # Celery Configuration
    CELERY_BROKER_URL = 'redis://localhost:6379/0'  # Redis URL for Celery broker
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'  # Redis URL for Celery result backend
    CELERY_TIMEZONE = 'Asia/Kolkata'  # Your timezone for periodic tasks
    CELERY_BEAT_SCHEDULE = {
        # Periodic task example: send daily reminders
        'send-daily-reminders': {
            'task': 'send_daily_reminders',
            'schedule': crontab(hour=20, minute=0),  # Schedule task to run at 8 PM every day
        },
        # Periodic task example: send monthly reports
        'send-monthly-report': {
            'task': 'send_monthly_report',
            'schedule': crontab(day_of_month=1, hour=0, minute=0),  # Schedule task for the 1st of each month at midnight
        },
    }
    
# Cache setup (using Redis for caching)
cache = Cache()
