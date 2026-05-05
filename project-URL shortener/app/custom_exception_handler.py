from .custom_exception import Database_Server_Exception
from .main import app
@app.exception_handler(Database_Server_Exception)
def app_exception_handler(exc:Database_Server_Exception):
    return JSONResponse(
        status_code=exc.status_code,content={
            "status":False,"error":exc.error,"detail":exc.detail
        }
    )
