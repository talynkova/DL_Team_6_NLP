from pydantic import BaseModel


class Vacancy(BaseModel):
    Vacancy: str
    Employer: str
    Vac_salary: bool
    Vac_salary_from: float
    Vac_salary_to: float
    Vac_exp: str
    Vac_schedule: str
    Vac_description: str
    Vac_prof_roles: str
    Vac_specializations: str
    Vac_profar_names: str
    Vac_keys: str


class Resume(BaseModel):
    CV_keys: str
    CV_name: str
    CV_specializations: str
    CV_profar_names: str
    CV_exp: str
    CV_schedule: str
    CV_employment: str
    CV_area_name: str
    CV_salary_from: float
    CV_salary_to: float


class JobRequest(BaseModel):
    vacancy: Vacancy
    resume: Resume
