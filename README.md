# WIP Entity Extraction Service API

This service is intended as a simple entity extraction (EE) API. The goal: input plaintext, extract entities, output structured entity document for backend to process.

Assumptions:
RequestBody.entity_types is either empty or well-formatted (meaning it is a valid list of real entities)
