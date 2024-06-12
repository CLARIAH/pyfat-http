from fastapi import FastAPI, Response, HTTPException
from starlette.requests import Request
import os
import subprocess

ttl_path: str = os.environ.get("TTL_PATH", "ttl")
html_path: str = os.environ.get("HTML_PATH", "html")
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
    ttl_record_full_path: str = os.path.join(ttl_path, f"{record_id}.ttl")
    trix_full_path: str = "trix/test.trix"
    if os.path.isfile(html_record_full_path):
        with open(html_record_full_path, "r") as file:
            return Response(content=file.read(), media_type='text/html')
    elif os.path.isfile(ttl_record_full_path):
        # Convert TTL to Trix to a fixed file
        subprocess.run(["./rdfconvert.sh", "-i", "Turtle", "-o", "Trix", ttl_record_full_path, trix_full_path])
        # Convert Trix to HTML(XML)
        subprocess.run(["./xsl.sh", "-xsl:FATtoHTML.xsl", f"-s:{trix_full_path}", f"-o:{html_record_full_path}"])
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

