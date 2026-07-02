from queues.worker import process_query
from client.rq_client import queue
from fastapi import FastAPI, Query

app = FastAPI()


@app.get("/")
def root():
    return {"status": "Server is up and running"}


@app.post("/chat")
def chat(query: str = Query(..., description="Chat query of user")):
    job = queue.enqueue(process_query, query)

    return {"status": "queued", "job_id": job.id}
