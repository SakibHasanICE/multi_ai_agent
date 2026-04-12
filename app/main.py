import subprocess
import time
import threading

from app.common.logger import get_logger
from app.common.custom_exception import CustomException
from dotenv import load_dotenv

logger =get_logger(__name__)

load_dotenv()

def run_backend():
    try:
        logger.info("startung backend service..")
        subprocess.run(["uvicorn","app.backend.api:app","--host","127.0.0.1","--port","9999"],check=True)
    
    except CustomException as e:
        logger.error("problem with backend service")
        raise CustomException("Failed to start backend",e)
    

def run_frontend():
    try:
        logger.info("starting frontend service")
        subprocess,run(["streamlit","run","app/frontend/ui.py"],check=True)

    except CustomException as e:
        logger.error("problem with frontend service")
        raise CustomException("Failed to start frontend",e)
    
if __name__=="__main__":
    try:
        threading.Thread(targetr=run_backend).start()
        time.sleep(2)
        run_frontend
    except CustomException as e:
        logger.exception(f"cusomexception occured :{str(e)}")


