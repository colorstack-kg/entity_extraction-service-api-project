from fastapi import FastAPI, Depends
from gliner2 import GLiNER2
from dotenv import load_dotenv
import os
from multiprocessing import Pool
from functools import partial

from auth import validate_auth
from models import ReqModel
from utils import *

load_dotenv()
MODEL_STRING = "fastino/gliner2-large-v1" if os.getenv("LARGE_MODEL") else "fastino/gliner2-base-v1"
NUM_PROC = int(os.getenv("NUM_PROC") or 0) or max(1, os.process_cpu_count() // 2)

_worker_extractor = None

def init_worker(model_string: str):
    """
    Runs once per worker process.
    """
    global _worker_extractor
    _worker_extractor = GLiNER2.from_pretrained(model_string)

def worker_extract(text: str, entity_types: dict[str, str] | list[str]):
    """
    Runs for each chunk.
    """
    schema = _worker_extractor.create_schema().entities(entity_types)
    return _worker_extractor.extract(
        text,
        schema,
        include_confidence=True,
    )

app = FastAPI()

POOL = None

@app.on_event("startup")
def startup_event():
    global POOL
    POOL = Pool(
        processes=NUM_PROC,
        initializer=init_worker,
        initargs=(MODEL_STRING,),
    )

@app.on_event("shutdown")
def shutdown_event():
    if POOL:
        POOL.close()
        POOL.join()

default_schema = {
    "organization": "Organization, company, or institution",
    "location": "Geographical area such as a city, country, region, facility, or named geographic feature",
    "time": "Date, day, HH:MM (hour:minute), or time period that should answer the question of 'when?'",
    "person": "Person",
    # "misc": "a miscellaneous named entity that cannot be classified into: [ORGANIZATION, LOCATION, TIME, PERSON, NUMBER] (such as events, works, laws, products, species, etc.)",
}

@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.post("/extract")
def extract_entities(req: ReqModel, api_key: str = Depends(validate_auth)):
    schema = req.entity_types or default_schema
    chunks = chunk_text(req.input_text)
    fn = partial(worker_extract, entity_types=schema)
    parts = POOL.map(fn, chunks)

    result = merge_parts(parts, schema)
    return result