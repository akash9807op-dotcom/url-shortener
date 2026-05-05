from app.main import app
import pytest
import json
import pytest
from app import models
from app.database import get_db
from fastapi.testclient import TestClient
client=TestClient(app)


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

database_url="postgresql://postgres:akash123@localhost:5431/test"
engine = create_engine(
    database_url,
    pool_size=5,
    max_overflow=10,
    pool_timeout=30,
    pool_recycle=1800,
)
models.Base.metadata.drop_all(bind=engine)
models.Base.metadata.create_all(bind=engine)
TestingSession=sessionmaker(bind=engine,autoflush=False,autocommit=False)
@pytest.fixture
def session():
    db=TestingSession()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture
def client(session):
    def override_get_db():
        db=TestingSession()
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db]=override_get_db
    yield TestClient(app)
keys=[]
@pytest.mark.parametrize("key", [
    "http://example.com/api/test",
    "https://example.org/data",
    "http://test.local/api/users",
    "https://api.sampleapis.com/coffee/hot",
    "https://jsonplaceholder.typicode.com/posts/3",
    "http://mockapi.io/projects/123/users",
    "https://httpbin.org/get",
    "https://httpbin.org/anything",
    "http://demo.testfire.net",
    "https://reqres.in/api/users/2",
    "http://numbersapi.com/random/trivia",
    "https://api.publicapis.org/entries",
    "https://dog.ceo/api/breeds/image/random",
    "https://catfact.ninja/fact",
])
def test_create_mini_url(key,client):
    res=client.post('/miniurl/',json={"url":key})
    print(res)
    extracted=res.json()["data"].split('/')[-1]
    print(extracted)
    keys.append((extracted))
    assert res.status_code==201

@pytest.mark.parametrize("key",keys)
def test_get_url(client, key):
    res = client.get(f"/miniurl/{key}")
    assert res.status_code == 200


invalid_urls = [
    "htp://google.com",          # wrong scheme
    "://missing-scheme.com",
    "http//missing-colon.com",
    "http:/one-slash.com",
    "justtext",
    "www.google.com",            # no scheme
    "http://",
    "https://?",
    "ftp:// space .com",
    "http://invalid_domain",
    "http://.com",
    "http://#fragment",
    "http://?query",
    "https://-badstart.com",
    "https://badend-.com",
    "http://256.256.256.256",
    "http://example..com",
    "http://.example.com",
    "https://example.com:abc",
    "random_string_123"
]
@pytest.mark.parametrize("key",invalid_urls)
def test_invalid_url(client,key):
    res=client.post('/miniurl/',json={"url":key})
    assert res.status_code==422


urls = [
    "http://localhost:8000/miniurl/a8f3K2",
    "http://localhost:8000/miniurl/xY72Lm",
    "http://localhost:8000/miniurl/pQ91az",
    "http://localhost:8000/miniurl/7sdK21",
    "http://localhost:8000/miniurl/Zx81Lp",
    "http://localhost:8000/miniurl/ab12CD",
    "http://localhost:8000/miniurl/k9Lm3P",
    "http://localhost:8000/miniurl/Qw82Er",
    "http://localhost:8000/miniurl/Ty91Ui",
    "http://localhost:8000/miniurl/mN45Op",
    "http://localhost:8000/miniurl/hJ73Ks",
    "http://localhost:8000/miniurl/vB61Qw",
    "http://localhost:8000/miniurl/Rt52Yu",
    "http://localhost:8000/miniurl/Lp84Gh",
    "http://localhost:8000/miniurl/We39Tr",
    "http://localhost:8000/miniurl/Xc74Bn",
    "http://localhost:8000/miniurl/Nm28Qa",
    "http://localhost:8000/miniurl/Ds62Fg",
    "http://localhost:8000/miniurl/Uy51Hv",
    "http://localhost:8000/miniurl/Jk90Pl",
]
@pytest.mark.parametrize("url", urls)
def test_get_url_not_found(url,client):
    res=client.get(url)
    assert res.status_code==404
def test_rate_limiting(client):
    res=None
    for _ in range(100):
        res=client.post("/miniurl/",json={"url":"http://example.com"})
    assert res.status_code==429