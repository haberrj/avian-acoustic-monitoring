from fastapi import FastAPI, Header, HTTPException

app = FastAPI()


@app.post("/detections/")
def create_detection(payload: dict, authorization: str | None = Header(default=None)):
    if authorization != "Bearer YOUR_TOKEN":
        raise HTTPException(status_code=401, detail="Unauthorized")

    # TODO: insert into Postgres
    return {"status": "ok"}