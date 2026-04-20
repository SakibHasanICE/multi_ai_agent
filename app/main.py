import subprocess
import time
import threading
import sys

from app.common.logger import get_logger
from app.common.custom_exception import CustomException
from dotenv import load_dotenv

logger = get_logger(__name__)

load_dotenv()

def run_backend():
    try:
        logger.info("Starting backend service on 0.0.0.0:9999")
        print("Starting backend service on 0.0.0.0:9999", flush=True)
        subprocess.run(
            [sys.executable, "-m", "uvicorn", "app.backend.api:app",
             "--host", "0.0.0.0", "--port", "9999"],
            check=True
        )
    except Exception as e:
        print(f"BACKEND FAILED TO START: {str(e)}", flush=True)
        logger.error(f"problem with backend service: {str(e)}")


def run_frontend():
    try:
        logger.info("Starting frontend service")
        print("Starting frontend service", flush=True)
        subprocess.run(
            [sys.executable, "-m", "streamlit", "run", "app/frontend/ui.py",
             "--server.address", "0.0.0.0",
             "--server.port", "8501"],
            check=True
        )
    except Exception as e:
        print(f"FRONTEND FAILED TO START: {str(e)}", flush=True)
        logger.error(f"problem with frontend service: {str(e)}")


if __name__ == "__main__":
    backend_thread = threading.Thread(target=run_backend, daemon=True)
    backend_thread.start()

    print("Waiting for backend to start...", flush=True)
    time.sleep(5)

    print("Starting frontend...", flush=True)
    run_frontend()