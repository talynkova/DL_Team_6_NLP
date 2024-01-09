# Проект по подбору резюме и вакансий 

Наш проект помогает понять, насколько конкретное резюме подходит к конкретной вакансии. На выходе после загрузки резюме и вакансии человек получает число, которое это показывает (в процентах).


## Содержание

- [Описание работы сервиса](#summary)
- [Архитектура сервиса](#architecture)
- [Deploy](#deploy)
- [Пример работы сервиса](#demo)
- [FAQ](#faq)
- [Команда проекта](#project-team)
- [Ссылки](#links)


### Summary

**Цель:** Создание сервиса для мэтчинга вакансий и резюме, чтобы упростить жизнь HR и оптимизировать часть рутинной работы.

**Данные:**  Все, что касается данных и работы с ними описано в ридми файлах каталога Data_preparing и ноутбуках, которые там находятся.

**Используемая модель и эксперименты:** На данный момент проведены эксперимент с `catboost` с различными гиперпараметрами. В качестве метрики используем `MAE`, лучший результат - 0.0157 (~1.6%).

**Дальнейшая работа:** Планируется лучше проработать бизнес-логику проекта (конкретно по составлению датасета для обучения - присуждать вес не только совпадающим скиллам, но еще и опыту работы, доменной области и т.д.). В идеале, если проект вызовет интерес у какой-нибудь компании, получить базу данных, в которой будут отражены вакансии, отклики на эту вакансию и класс-метка, который отвечает за то, пригласили ли кандидата на собеседование. Найти такие БД в открытом доступе не получилось, был только один вариант [здесь, датасет 3](https://trudvsem.ru/opendata/datasets), но там оказалась битая ссылка на базу описания вакансий, а сотрудничать с нами никто из данной организации не захотел.


## Architecture

Здесь будет находиться архитектура сервиса.


## Deploy

Для запуска сервиса нужно выполнять следующие команды: 
- Клонируйте данный репозиторий
- `pip install -r requirements.txt` 
- `cd inference_api`
- `uvicorn main:app`

## Demo

### Пример запроса
**`POST /career/score`**
Метод принимает информацию о вакансии и о резюме, и возвращает релевантность этой вакансии для резюме

```json
{
    "vacancy":{
        "Vacancy": "Golang Developer (Кипр)",
        "Employer": "Space307",
        "Vac_salary": "True", 
        "Vac_salary_from": 251322.0,
        "Vac_salary_to": 0,
        "Vac_exp": "От 3 до 6 лет",
        "Vac_schedule": "Полный день",
        "Vac_description": "Мы в Space307 разрабатываем международную",
        "Vac_prof_roles": "['Программист', 'разработчик']",
        "Vac_specializations": "['Программирование', 'Разработка']",
        "Vac_profar_names": "['Информационные технологии', 'интернет']",
        "Vac_keys": "['Docker', 'Golang', 'Redis']"
    },
    "resume":{
        "CV_name": "Middle Golang Developer",
        "CV_salary_from": 251322.0,
        "CV_salary_to": 0,
        "CV_exp": "От 1 до 3 лет",
        "CV_employment": "Полный день",
        "CV_schedule": "Полный день",
        "CV_area_name": "Москва",
        "CV_prof_roles": "['Программист', 'разработчик']",
        "CV_specializations": "['Программирование', 'Разработка']",
        "CV_profar_names": "['Информационные технологии'']",
        "CV_keys": "['Git', 'Golang', 'Rabbitmq']"
    }
}

```
```json

{
    "vacancy": {
        "name": "Golang Developer (Кипр)",
        "employer": "Space307",
        "schedule": "Полный день"
    },
    "resume": {
        "name": "Middle Golang Developer",
        "specializations": "['Программирование', 'Разработка']",
        "keys": "['Git', 'Golang', 'Rabbitmq']"
    },
    "score": 0.021916874830105362
}

```
## FAQ

На данный момент нами не было выявлено никаких проблем в работе проекта. Если вдруг Вы столкнётесь с проблемой - пожалуйста, напишите кому-нибудь из команды проекта в LinkedIn, мы обещаем посмотреть и разобраться!


## Project team
- DE - [Siniaev Viacheslav](https://www.linkedin.com/in/vyacheslavsinyaev/) 
- ML - 
- Back-end - [Mulham Shahin](https://www.linkedin.com/in/mulham-shaheen-684352206/)
- Full stack - Elizaveta Talynkova
- Full stack - [Nikita Bekasov](https://www.linkedin.com/in/nibekasov/)


## Links
- Ссылка на лучшую [модель:](https://drive.google.com/file/d/1-dLs11Bx-UzeK62gRoHgGAmC9WTxn284/view)
- Ссылка на итоговый [датасет](https://drive.google.com/file/d/1oQPNTh9uCebatw5w2Ycqn-cezpZ_eq03/view?usp=sharing)
