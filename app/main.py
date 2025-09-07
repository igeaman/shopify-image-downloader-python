from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
import logging.config

from app.routers import shopify

# Logging dictionary
LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        }
    },
    'handlers': {
        'file': {
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'formatter': 'standard',
            'filename': 'app.log',
            'when': 'midnight',
            'interval': 1,
            'backupCount': 7,
            'encoding': 'utf8'
        }
    },
    'loggers': {
        'root': {
            'level': 'INFO',
            'handlers': ['file']
        },
        'uvicorn.error': {
            'level': 'INFO',
            'handlers': ['file']
        },
        'uvicorn.access': {
            'level': 'INFO',
            'handlers': ['file']
        },
    },
}

# apply the loggin configuration

logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)
logger.info("Server Started!!!",)


def create_app() -> FastAPI:
    app = FastAPI(title="Shopify Image Downloader Python Backend", version="1.0.0")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers
        =["*"],
    )


    @app.get("/health")
    async def health_check():
        return {"status": "ok"} 
    
    app.include_router(shopify.router)

    return app


app = create_app()

# uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

