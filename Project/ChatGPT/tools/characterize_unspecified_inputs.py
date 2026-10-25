"""Non-assertive characterization of underspecified business rules."""
import json
import tempfile
from pathlib import Path
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.database import Base, get_db
from main import app

with tempfile.TemporaryDirectory(prefix="todo_unspecified_") as temp:
    engine=create_engine(f"sqlite:///{Path(temp)/'characterization.sqlite3'}",connect_args={"check_same_thread":False})
    Base.metadata.create_all(engine)
    Session=sessionmaker(bind=engine)
    def override():
        session=Session()
        try: yield session
        finally: session.close()
    app.dependency_overrides[get_db]=override
    try:
        with TestClient(app,raise_server_exceptions=False) as c:
            for i in range(12):
                assert c.post('/todos/',json={'title':f'example-{i}'}).status_code==200
            observations={}
            for q in ['limit=-1', 'limit=0', 'skip=-1', 'skip=-2', 'limit=100000']:
                r=c.get('/todos/?'+q)
                observations[q]={'status':r.status_code, 'count':len(r.json()) if r.status_code==200 else None}
            for label,payload in [('blank_title',{'title':''}),('whitespace_title',{'title':'  '}),('unexpected_status',{'title':'x','status':'some-made-up-status'})]:
                r=c.post('/todos/',json=payload)
                observations[label]={'status':r.status_code, 'body':r.json() if r.status_code==200 else r.text}
            print(json.dumps(observations,ensure_ascii=False,indent=2))
    finally:
        app.dependency_overrides.clear()
        engine.dispose()
