from fastapi import FastAPI
import os
import sys
import json

app = FastAPI()

@app.get("/")
async def root():
    return {
        "message": "Hello World",
        "environment": dict(os.environ),
        "python_version": sys.version,
        "sys_path": sys.path
    }

@app.get("/debug")
async def debug():
    try:
        # Return info about the environment
        return {
            "message": "Debug information",
            "cwd": os.getcwd(),
            "files_in_cwd": os.listdir(),
            "sys_path": sys.path,
        }
    except Exception as e:
        return {"error": str(e), "error_type": type(e).__name__}