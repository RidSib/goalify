# Step 1: Code your own function to talk to a third party API or database

import os
import requests
from restack_ai.function import function, log
from pydantic import BaseModel

class FunctionInput(BaseModel):
    message: str

class FunctionOutput(BaseModel):
    response: str

@function.defn()
async def txt_import(input: FunctionInput) -> FunctionOutput:
    try:
        log.info("txt import started", input=input)

        # TODO: Implement the logic for the function like talking to a third party API or database

        response_message = f"Received message: {input.message}"
        return FunctionOutput(response=response_message)
    except Exception as e:
        log.error("txt import failed", error=e)
        raise e
