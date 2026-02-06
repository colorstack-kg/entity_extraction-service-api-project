from fastapi import FastAPI, Depends
from gliner2 import GLiNER2

from auth import validate_auth
from models import ReqModel

app = FastAPI()
extractor = GLiNER2.from_pretrained("fastino/gliner2-base-v1")

default_schema = extractor.create_schema().entities({
    "organization": "Organization, company, or institution",
    "location": "Geographical area such as a city, country, region, facility, or named geographic feature",
    "time": "Date, day, hour/minute, point in time, era, or period that should answer the question of 'when?'",
    "person": "Person",
    # "misc": "a miscellaneous named entity that cannot be classified into: [ORGANIZATION, LOCATION, TIME, PERSON, NUMBER] (such as events, works, laws, products, species, etc.)",
})

@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.post("/extract")
def extract_entities(req: ReqModel, api_key: str = Depends(validate_auth)):
    if not req.entity_types:
        schema = default_schema
    else:
        schema = extractor.create_schema().entities(req.entity_types)

    result = extractor.extract(
        req.input_text,
        schema,
        include_confidence=True
    )

    return result