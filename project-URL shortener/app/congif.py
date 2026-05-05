from pydantic import BaseSettings
class Settings(BaseSettings):
    dbname:str
    port:int 
    host:str
    password:str
    user:str
    class Config():
        env_file=".env"
setting=Settings()