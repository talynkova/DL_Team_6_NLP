from dataclasses import dataclass, asdict
import logging
import pandas as pd
import numpy as np
from catboost import Pool
from catboost import CatBoostRegressor

from .models import Vacancy, Resume


@dataclass
class RecoResult:
    resume: Resume
    vacancy: Vacancy
    score: float

    def dict(self):
        return {
            "vacancy": {
                "name": self.vacancy.Vacancy,
                "employer": self.vacancy.Employer,
                "schedule": self.vacancy.Vac_schedule,
            },
            "resume": {
                "name": self.resume.CV_name,
                "specializations": self.resume.CV_specializations,
                "keys": self.resume.CV_keys,
            },
            "score": self.score,
        }


class CatBoostRecommender:
    def __init__(self, model_path: str = "catboost_model"):
        logging.info('Loading Detector')
        self.model = CatBoostRegressor()
        self.model_path = model_path
        self.load_model()

    def load_model(self):
        self.model.load_model(self.model_path)
        return self.model

    @staticmethod
    def preprocess_data(vacancy: Vacancy, resume: Resume) -> pd.DataFrame:
        vac_data = vacancy.model_dump()
        res_data = resume.model_dump()
        vac_df = pd.DataFrame(data=[vac_data])

        res_df = pd.DataFrame(data=[res_data])

        vac_df['Vac_salary_from'] = pd.to_numeric(
            vac_df['Vac_salary_from'].apply(lambda x: x if x != "Не указана" else np.NaN))
        vac_df['Vac_salary_to'] = pd.to_numeric(
            vac_df['Vac_salary_to'].apply(lambda x: x if x != "Не указана" else np.NaN))

        df = pd.concat([vac_df, res_df], axis=1, ignore_index=False)
        return df

    def recommend(self, vacancy: Vacancy, resume: Resume):
        df_prep = self.preprocess_data(vacancy, resume)
        pred = self.model.predict(df_prep)[0]
        pred_clipped = np.clip(pred, 0, 1)
        return pred_clipped.item()
