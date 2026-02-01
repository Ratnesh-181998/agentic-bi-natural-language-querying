from sqlalchemy import create_engine, text
engine = create_engine("sqlite:///enterprise_bi_db.sqlite")

def run(state):
    with engine.connect() as conn:
        res = conn.execute(text(state["sql"]))
        # Convert to list of dicts for easier downstream processing
        state["result"] = [dict(row._mapping) for row in res]
    return state
