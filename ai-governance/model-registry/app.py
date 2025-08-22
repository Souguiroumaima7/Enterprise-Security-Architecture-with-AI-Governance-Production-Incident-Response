from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3
import uuid
import time
import os
import json

DB = os.getenv('MODEL_DB', '/data/models.db')

class Model(BaseModel):
    name: str
    version: str
    dataset: str
    metrics: dict
    owner: str

app = FastAPI(title='Model Registry')

def init_db():
    conn = sqlite3.connect(DB)
    conn.execute('''
        CREATE TABLE IF NOT EXISTS models (
            id TEXT PRIMARY KEY,
            name TEXT,
            version TEXT,
            dataset TEXT,
            metrics TEXT,
            owner TEXT,
            created_at INTEGER
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.post('/models')
async def register_model(m: Model):
    conn = sqlite3.connect(DB)
    model_id = str(uuid.uuid4())
    conn.execute(
        'INSERT INTO models VALUES (?,?,?,?,?,?,?)',
        (model_id, m.name, m.version, m.dataset, json.dumps(m.metrics), m.owner, int(time.time()))
    )
    conn.commit()
    conn.close()
    return {'id': model_id, 'status': 'registered'}

@app.get('/models')
async def list_models():
    conn = sqlite3.connect(DB)
    rows = conn.execute(
        'SELECT id, name, version, dataset, metrics, owner, created_at FROM models'
    ).fetchall()
    conn.close()
    return [
        {
            'id': r[0],
            'name': r[1],
            'version': r[2],
            'dataset': r[3],
            'metrics': json.loads(r[4]),
            'owner': r[5],
            'created_at': r[6]
        }
        for r in rows
    ]
@app.get('/models/{model_id}')
async def get_model(model_id: str):
    conn = sqlite3.connect(DB)
    row = conn.execute(
        'SELECT id, name, version, dataset, metrics, owner, created_at FROM models WHERE id=?',
        (model_id,)
    ).fetchone()
    conn.close()
    if not row:
        raise HTTPException(status_code=404, detail='Model not found')
    return {
        'id': row[0],
        'name': row[1],
        'version': row[2],
        'dataset': row[3],
        'metrics': json.loads(row[4]),
        'owner': row[5],
        'created_at': row[6]
    }