import os
from fastapi import FastAPI, UploadFile, File
from .infrustructure.catboost_recomender import CatBoostRecommender, RecoResult
from .infrustructure.models import JobRequest

app = FastAPI()
UPLOAD_PATH = "uploads"

recommender = CatBoostRecommender(model_path="inference_api/saved_models/catboost_model")


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/career/score")
async def predict_score(request: JobRequest):
    vacancy = request.vacancy
    resume = request.resume
    score = recommender.recommend(vacancy, resume)

    res = RecoResult(resume, vacancy, score)

    return res.dict()
