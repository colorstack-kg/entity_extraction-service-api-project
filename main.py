from fastapi import FastAPI, Depends
from gliner2 import GLiNER2

from auth import validate_auth
from models import ReqModel

app = FastAPI()
extractor = GLiNER2.from_pretrained("fastino/gliner2-base-v1")

# default_schema = extractor.create_schema().entities({
#     "organization": "Group, company, or institution",
#     "location": "Geographical area such as a city, country, region, facility, or named geographic feature",
#     "time": "Date, day, hour/minute, point in time, or period that should answer the question of when",
#     "person": "Person",
#     # "misc": "a miscellaneous named entity that cannot be classified into: [ORGANIZATION, LOCATION, TIME, PERSON, NUMBER] (such as events, works, laws, products, species, etc.)",
# })
default_schema = ["organization", "location", "time", "person"]

@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.post("/extract")
def extract_entities(req: ReqModel, api_key: str = Depends(validate_auth)):
    # TODO: create a schema based off of req.entity_types and observe difference in output if there is any 😼
    # TODO: mock extractor so that I can test functionality without needing the RAM of GLiNER
    # TODO: append logs to logfile
    result = extractor.extract_entities(
        req.input_text,
        req.entity_types or default_schema,
        include_confidence=True
    )

    return result