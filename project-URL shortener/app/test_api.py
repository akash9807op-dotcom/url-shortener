# from fastapi import FastAPI
# import time
# import asyncio
# from datetime import datetime
# app=FastAPI()
# ps=0
# @app.get('/')
# def root():
#     global ps
#     current_ps= ps
#     print(f"start at Process id {current_ps} at {datetime.now()}")    
#     time.sleep(5)
#     print(f"its over Process id {current_ps} at {datetime.now()}")    
#     ps+=1


import threading
import time
from datetime import datetime
start=datetime.now()
def do_some():
    print("It start")
    time.sleep(2)
    print("it ended")
th=[]
for _ in range(300):
    t=threading.Thread(target=do_some)
    th.append(t)
    t.start()
for t in th:
    t.join()

print("COmpleted in ",datetime.now()-start)




















































# from .import main
# import json
# # class Test:
#     # @classmethod
#     # def test_create_url(self):
#     #     input={"url":"https://www.youtube.com/results?search_query=dsa+project+idea+"}
#     #     result=main.url_shortner(input)
#     #     print(result,flush=False)
#     #     assert result["success"]==True

#     # @classmethod
#     # def test_get_url(self):
#     #     input="2Bk"
#     #     result=main.get_url(input)
#     #     print(result,flush=False)
#     #     assert result["success"]==True
# import pytest
# from fastapi.testclient import TestClient
# from app.main import app

# client = TestClient(app)


# def test_root():
#     response = client.get("/")
#     assert response.status_code == 200
#     data = response.json()

#     assert data["success"] is True
#     assert data["data"] == "This is Root page"


# # def test_create_short_url():
# #     payload = {
# #         "url": "https://google.com"
# #     }

# #     response = client.post("/miniurl", json=payload)

# #     assert response.status_code == 200
# #     data = response.json()

# #     assert data["success"] is True
# #     assert "miniurl" in data["data"]


# # def test_get_url():
# #     payload = {"url": "https://example.com"}

# #     create = client.post("/miniurl", json=payload)
# #     short_url = create.json()["data"]

# #     key = short_url.split("/")[-1]

# #     response = client.get(f"/miniurl/{key}")

# #     assert response.status_code == 200
# #     data = response.json()

# #     assert data["success"] is True
# #     assert data["data"] == "https://example.com"



# def test_get_url_not_found():
#     response = client.get("/miniurl/invalidkey")

#     assert response.status_code == 404


