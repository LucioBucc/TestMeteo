import uvicorn
import time
from fastapi import FastAPI, HTTPException, Request
from app.routes import r_sites
from app.middleware.db import engine, SessionLocal
from app import models
from mangum import Mangum


description = """
Meteo per latitudine longitudine API. 🚀
"""

app = FastAPI(
    title="Meteo API",
    description=description,
    version="0.0.1",
    openapi_url="/v1/openapi.json",
    docs_url=None,
    redoc_url=None,
    debug=True
)


models.Base.metadata.create_all(bind=engine)

app.include_router(r_sites.router, prefix="/api/v1")

@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

handler = Mangum(app)

'''def run(*, in_host="0.0.0.0", in_port=80, in_reload=True):
    uvicorn.run("main:app", host=in_host, port=in_port, reload=in_reload)


if __name__ == '__main__':
    run(in_port=8000)
'''