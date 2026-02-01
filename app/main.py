from fastapi import FastAPI
from app.langgraph.graph import bi_graph
from app.billing.metering import record_usage
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

@app.post("/ask")
def ask(payload: dict):
    try:
        result = bi_graph.invoke(payload)
        record_usage(payload["tenant_id"], "query", 1)
        return result["response"]
    except Exception as e:
        import traceback
        traceback.print_exc()
        return {"error": str(e), "status": "failed"}
