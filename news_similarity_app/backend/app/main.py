from fastapi import FastAPI
from . import api, models, database, scheduler

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()
app.include_router(api.router)
scheduler.start_scheduler()