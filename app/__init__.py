import os
import logging
from logging.handlers import RotatingFileHandler
from flask import Flask
from app.data_ingestor import DataIngestor
from app.task_runner import ThreadPool

# Determinăm calea către fișierul de log
log_file_path = os.path.join("logs", "webserver.log")

# Verificăm dacă fișierul există
if os.path.exists(log_file_path):
    # Ștergem conținutul fișierului
    with open(log_file_path, "w", encoding="utf-8"):
        pass

# Creăm o instanță de Flask
webserver = Flask(__name__)

# Configurăm logger-ul pentru a scrie în fișierele .log din folderul "logs"
LOG_FORMAT = "%(asctime)s [%(levelname)s] %(message)s"
# Folosim nivelul de logging INFO
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)

# 10 MB max per file, keep 5 files
handler = RotatingFileHandler(log_file_path, maxBytes=10*1024*1024, backupCount=5)
handler.setFormatter(logging.Formatter(LOG_FORMAT))

# Adăugăm handler-ul la logger-ul instanței de Flask
webserver.logger.addHandler(handler)

# Pornesc ThreadPool-ul si thread-urile
webserver.tasks_runner = ThreadPool()
webserver.tasks_runner.start()

webserver.data_ingestor = DataIngestor("./nutrition_activity_obesity_usa_subset.csv")

from app import routes
