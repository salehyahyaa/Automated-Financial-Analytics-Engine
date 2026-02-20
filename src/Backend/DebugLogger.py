import json
import time
import os
"""
Handles debug logging across codebase, tracks endpoints sucss/err @runtime. composition to avoid redundant code
"""


class DebugLogger:
    
    # Default log file path - can be overridden in __init__
    DEFAULT_LOG_PATH = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        ".logs",
        "debug.log"
    )
    

    def __init__(self, log_file_path=None):             #log_file_path (str, optional): Path to the debug log file If None, uses DEFAULT_LOG_PATH.
        self.log_file_path = log_file_path or self.DEFAULT_LOG_PATH
    
    
    def log_error(self, location, exception):                              #location(str): Location identifier (e.g., "Endpoints.py:functionName")
        try:
            with open(self.log_file_path, "a") as f:
                f.write(json.dumps({
                    "location": location,
                    "message": "exception",
                    "data": {
                        "type": type(exception).__name__,
                        "msg": str(exception)
                    },
                    "timestamp": round(time.time() * 1000),
                    "hypothesisId": "D"
                }) + "\n")
        except Exception:                                                  # Fail silently - don't break API if logging fails
            pass
