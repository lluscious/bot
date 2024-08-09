import os
import shutil
from util.log import logger

class cache:

    def clear_cache():
        clearNum = 0
        for root, dirs, files in os.walk(os.getcwd()):
            if '__pycache__' in dirs:
                shutil.rmtree(os.path.join(root, '__pycache__'))
                clearNum = clearNum+1
        logger.log(f"Cleared {clearNum} cache folders")