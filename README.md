# WIP Entity Extraction Service API

This service is intended as a simple entity extraction (EE) API. The goal: input plaintext, extract entities, output structured entity document for backend to process.

### Service Deployment Instructions:
1. clone repo
1. set up .env file
1. Docker command: `docker run -d -v ~/.cache/huggingface:/root/.cache/huggingface -p 8000:8000 --env-file .env <image_name>`

### Assumptions:
RequestBody.entity_types is either empty or well-formatted (meaning it is a valid list of real entities)

Feel free to ask me if you are confused on anything!