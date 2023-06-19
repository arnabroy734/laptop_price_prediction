from dotenv import load_dotenv
load_dotenv()
import os
from pymongo import MongoClient
from datetime import datetime

class SaveLogs:

    def __init__(self):
        try:
            client = MongoClient(os.environ['CONN_URL'])
            db = client[os.environ['DB']]
            self.collection = db[os.environ['APP_LOGS']]
        except Exception as e:
            print(f"SaveLogs: Database connection failed {e}")


    def savelog(self, module, msg_type, message):
        log = {
            "timestamp" : datetime.now(),
            "module" : module,
            "type" : msg_type,
            "message" : message
        }
        try:
            self.collection.insert_one(log)
        except Exception as e:
            print(f"SaveLogs: log cannot be saved {e}")

    def find_logs(self, module=None, msg_type=None):
        try:
            query = {}
            if module is not None:
                query["module"] = module
            if msg_type is not None:
                query["type"] = msg_type
            
            res = self.collection.find(query)
            return list(res)
        except Exception as e:
            print(f"SaveLogs: logs cannot be retrieved {e}")