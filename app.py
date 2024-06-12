from fastapi import FastAPI, Response, HTTPException
from starlette.requests import Request
import os
import uvicorn
import subprocess

ttl_path: str = "ttl"
html_path: str = "html"
app = FastAPI()


@app.get("/{record_id}")
async def get_record(request: Request, record_id: str):
    accept_header = request.headers.get('accept')

    ttl_record_full_path: str = os.path.join(ttl_path, f"{record_id}.ttl")
    html_record_full_path: str = os.path.join(html_path, f"{record_id}.xml")

    if accept_header == 'text/html':
        if os.path.exists(html_record_full_path) and os.path.isfile(html_record_full_path):
            with open(html_record_full_path, "r") as file:
                return Response(content=file.read(), media_type='text/html')
        else:
            raise HTTPException(status_code=404, detail=f"Record {html_record_full_path} not found as HTML and TTL files not found")

    else:
        if os.path.exists(ttl_record_full_path) and os.path.isfile(ttl_record_full_path):
            with open(ttl_record_full_path, "r") as file:
                return Response(content=file.read(), media_type='text/turtle')
        else:
            raise HTTPException(status_code=404, detail=f"Record {ttl_record_full_path} not found as TTL file not found")


@app.get("/html/{record_id}")
async def get_html_record(record_id: str):
    html_record_full_path: str = os.path.join(html_path, f"{record_id}.xml")
    if os.path.exists(html_record_full_path) and os.path.isfile(html_record_full_path):
        with open(html_record_full_path, "r") as file:
            return Response(content=file.read(), media_type='text/html')
    else:
        raise HTTPException(status_code=404, detail=f"Record {html_record_full_path} not found as HTML files not found")


@app.get("/ttl/{record_id}")
async def get_ttl_record(record_id: str):
    ttl_record_full_path: str = os.path.join(ttl_path, f"{record_id}.ttl")
    if os.path.exists(ttl_record_full_path) and os.path.isfile(ttl_record_full_path):
        with open(ttl_record_full_path, "r") as file:
            return Response(content=file.read(), media_type='text/turtle')
    else:
        raise HTTPException(status_code=404, detail=f"Record {ttl_record_full_path} not found as TTL file not found")

