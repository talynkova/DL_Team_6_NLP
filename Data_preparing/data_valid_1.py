#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd

print('Success')


# # Vacancies part

# ## Загрузка таблицы

# In[2]:


data1 = pd.read_csv('datasets/IT_vacancies_full.csv', header=0)


# In[3]:


data1


# ## Первичный анализ данных

# **Можно удалить самые неинформативные столбцы - айди и дату публикации**

# In[4]:


data1 = data1.drop(columns=['Ids', 'Published at'])


# ### Небольшая сводка по имеющимя данным

# In[5]:


print('Вакансии есть в следующих городах:',
      data1['Area'].unique())
print('Представлены вакансии для специалистов со следующим уровнем работы: ',
      data1['Experience'].unique())
print('Представлены следующие возможности графика работы: ',
      data1['Schedule'].unique())


# In[6]:


i = 0
j = 48563
for id in data1['Salary']:
    if not id:
        i += 1
print(f'Без указания зарплаты есть {i} позиций')
print(f'C указанием зарплаты есть {j-i} позиций')


# In[7]:


i = 0
j = 48563
for id in data1['Schedule']:
    if (id == 'Удаленная работа'):
        i += 1
print(f'С удалёнкой есть {i} позиций')
print(f'В офисе есть {j-i} позиций')


# In[8]:


i = 0
j = 48563
for id in data1['Area']:
    if (id == 'Москва'):
        i += 1
print(f'В Москве есть {i} позиций')
print(f'В Санкт-Петербурге есть {j-i} позиций')


# In[9]:


print('Самые популярные навыки для поиска в процентах: ',
      data1['Keys'].value_counts(1)*100)


# **У 17% вакансий не указаны требуемые навыки, это плохо, попробуем отказаться от этих вакансий**

# In[10]:


data1 = data1.loc[data1['Keys'] != '[]']


# **Для наглядности изобразим разброс зарплат**

# In[11]:


print('Границы зарплат: ')
data1.hist(figsize=(15, 7.5), grid=False, sharex=True)


# In[12]:


round(data1['From'].describe())


# In[13]:


round(data1['To'].describe())


# **Теперь посмотрим, кого ищут чаще всего и сколько всего уникальных должностей у нас есть**

# In[14]:


data1['Professional roles'].describe()


# In[15]:


data1['Professional roles'].value_counts(1)*100


# **Итого половина вакансий предназначена всего для трех специалистов - программиста, аналитика и тестировщика**

# In[16]:


data1['Profarea names'].describe()


# In[17]:


data1['Profarea names'].value_counts(1)*100


# **Как видно, большинство вакансий в датасете действительно из IT-компаний**

# ### Исправим пропущенные значения

# In[18]:


data1.isna().sum()


# In[19]:


data1['From'] = data1['From'].fillna("Не указана")
data1['To'] = data1['To'].fillna("Не указана")


# In[20]:


data1


# ### Откажемся от работодателей, которые не указывают зарплату

# **Но на всякий случай, сделаем это в отдельном фрейме**

# In[21]:


data_salary = data1.loc[data1['Salary'] != False]


# In[22]:


data_salary


# In[23]:


data_salary = data_salary.drop(columns=['Salary'])


# In[24]:


data_salary.info()


# **Немного видоизменим хранение навыков**

# In[25]:


def rename_skills(row):
    return row[1:-1]


# In[26]:


data1['Keys'] = data1['Keys'].apply(rename_skills)
data1['Professional roles'] = data1['Professional roles'].apply(rename_skills)
data1['Specializations'] = data1['Specializations'].apply(rename_skills)
data1['Profarea names'] = data1['Profarea names'].apply(rename_skills)


# In[27]:


data1


# In[28]:


data1


# In[29]:


data_salary['Keys'][0] = data_salary['Keys'][0][1:-1]


# In[30]:


data_salary['Keys'][0]


# # CV's part

# ## Загрузка таблицы

# In[31]:


data_cv = pd.read_csv('datasets/final_test.csv', header=0)


# In[32]:


data_cv


# ## Первичный анализ данных

# **Имеем большое количество объективно избыточной для нашей задачи информации, удалим её**

# In[33]:


data_cv = data_cv.drop(columns=['Unnamed: 0', 'id', 'accept_temporary',
                               'specializations_id', 'specializations_profarea_id',
                               'working_time_intervals_count', 'working_time_intervals_id',
                               'working_time_intervals_name', 'working_time_modes_id',
                               'working_time_modes_name', 'working_days_count',
                               'working_days_id', 'working_days_name',
                               'working_time_modes_count', 'area_id',
                               'experience_id', 'schedule_id', 'employment_id',
                               'currency', 'gross', 'specializations_count'])


# In[34]:


data_cv


# In[35]:


print('Самые популярные навыки у соискателей в процентах: ',
      data_cv['key_skills'].value_counts(1)*100)


# **В 30% вакансий не указаны требуемые навыки, это плохо, попробуем отказаться от этих резюме**

# In[36]:


data_cv = data_cv.loc[data_cv['key_skills'] != '[]']


# In[37]:


data_cv


# In[38]:


data_cv['key_skills'][3]


# **Необходимо привести стобец *key_skills* в нормальный вид (как в датасете с резюме)**

# In[39]:


input_string = data_cv['key_skills'][3]

# Разбор строки в структуру данных Python
skills_list = eval(input_string)

# Извлечение названий навыков и форматирование новой строки
formatted_string = ", ".join([f"'{skill['name']}'" for skill in skills_list])

# Вывод результата
print(formatted_string)


# **Теперь используем этот алгоритм для всех значений**

# In[40]:


def transform_skills(skill):
    skills_list = eval(skill)
    formatted_string = ", ".join([f"'{skill['name']}'" for skill in skills_list])
    return formatted_string


# In[41]:


data_cv = data_cv.reset_index()


# In[42]:


data_cv['key_skills'] = data_cv['key_skills'].apply(transform_skills)


# In[44]:


data_cv['Keys_new_cv'] = data_cv['key_skills'].apply(lambda x: [skill.strip("'").strip() for skill in x.split(',')])
data1['Keys_new_vac'] = data1['Keys'].apply(lambda x: [skill.strip("'").strip() for skill in x.split(',')])
data1['Professional roles'] = data1['Professional roles'].apply(lambda x: [skill.strip("'").strip() for skill in x.split(',')])
data1['Specializations'] = data1['Specializations'].apply(lambda x: [skill.strip("'").strip() for skill in x.split(',')])
data1['Profarea names'] = data1['Profarea names'].apply(lambda x: [skill.strip("'").strip() for skill in x.split(',')])


# In[45]:


data_cv


# In[46]:


data_cv = data_cv.drop(columns=['index'])


# In[47]:


print(data_cv['key_skills'][0])
print(data_cv['key_skills'].dtype)


# **Для красоты изменим имена столбцов в формат первой таблицы**

# In[48]:


data_cv = data_cv.rename(columns={'key_skills': 'Keys',
                                  'salary_from': 'From',
                                  'salary_to': 'To',
                                  'name': 'Name',
                                  'schedule_name': 'Schedule',
                                  'specializations_profarea_name' : 'Profarea names',
                                  'experience_name' : 'Experience',
                                  'specializations_name': 'Specializations'})


# In[49]:


data_cv['Specializations'] = data_cv['Specializations'].apply(rename_skills)
data_cv['Profarea names'] = data_cv['Profarea names'].apply(rename_skills)


# In[50]:


data_cv['Keys'][0]


# In[51]:


print("Вакансии:")
print(list(data1))
print("Резюме:")
print(list(data_cv))


# In[ ]:





# ## Составление новой таблицы

# Здесь попытаемся создать итоговою таблицу, которая будет хранить в себе пары резюме-вакансии по лучшим совпадениям среди скиллов и информацию о том, насколько они совпадают.

# In[ ]:





# In[52]:


data_cv['Keys'].apply(lambda x: [skill.strip("'").strip() for skill in x.split(',')])[0][2]


# In[67]:


data1 = data1.reset_index()


# In[68]:


del data1['index']
#del data1['level_0']


# In[ ]:


result_dict = {}

# Итерация по вакансиям и резюме для нахождения соответствий
result_columns = [
    'Vacancy', 'Employer', 'Vac_salary', 'Vac_salary_from', 'Vac_salary_to',
    'Vac_exp', 'Vac_schedule', 'Vac_description', 'Vac_prof_roles',
    'Vac_specializations', 'Vac_profar_names', 'Vac_keys', 'CV_keys', 'CV_name',
    'CV_specializations', 'CV_profar_names', 'CV_exp', 'CV_schedule',
    'CV_employment', 'CV_area_name', 'CV_salary_from', 'CV_salary_to',
    'Matching_Skills'
]
result = pd.DataFrame(columns=result_columns)

# Итерация по вакансиям и резюме для нахождения соответствий
for index_vacancy, row_vacancy in data1.iterrows():
    best_matching_resume_index = None
    best_matching_score = 0
    
    for index_resume, row_resume in data_cv.iterrows():
        matching_skills = len(set(row_vacancy['Keys_new_vac']).intersection(row_resume['Keys_new_cv']))

        # Если нашли лучшее сочетание, обновляем переменные
        if matching_skills * 10 > best_matching_score:
            best_matching_resume_index = index_resume
            best_matching_score = matching_skills * 10

    # Если подходящее резюме не найдено, пропускаем текущую вакансию
    if best_matching_resume_index is not None:
        # Создаем уникальный ключ для комбинации вакансии и резюме
        key = (row_vacancy['Name'], data_cv.loc[best_matching_resume_index, 'Name'])

        # Добавляем сочетание в датафрейм только если резюме еще не использовано
        if key not in zip(result['Vacancy'], result['CV_name']):
            result = pd.concat([result, pd.DataFrame({
                'Vacancy': [row_vacancy['Name']],
                'Employer': [row_vacancy['Employer']],
                'Vac_salary': [row_vacancy['Salary']],
                'Vac_salary_from': [row_vacancy['From']],
                'Vac_salary_to': [row_vacancy['To']],
                'Vac_exp': [row_vacancy['Experience']],
                'Vac_schedule': [row_vacancy['Schedule']],
                'Vac_description': [row_vacancy['Description']],
                'Vac_prof_roles': [row_vacancy['Professional roles']],
                'Vac_specializations': [row_vacancy['Specializations']],
                'Vac_profar_names': [row_vacancy['Profarea names']],
                'Vac_keys': [row_vacancy['Keys_new_vac']],
                'CV_keys': [data_cv.loc[best_matching_resume_index, 'Keys_new_cv']],
                'CV_name': [data_cv.loc[best_matching_resume_index, 'Name']],
                'CV_specializations': [data_cv.loc[best_matching_resume_index, 'Specializations']],
                'CV_profar_names': [data_cv.loc[best_matching_resume_index, 'Profarea names']],
                'CV_exp': [data_cv.loc[best_matching_resume_index, 'Experience']],
                'CV_schedule': [data_cv.loc[best_matching_resume_index, 'Schedule']],
                'CV_employment': [data_cv.loc[best_matching_resume_index, 'employment_name']],
                'CV_area_name': [data_cv.loc[best_matching_resume_index, 'area_name']],
                'CV_salary_from': [data_cv.loc[best_matching_resume_index, 'From']],
                'CV_salary_to': [data_cv.loc[best_matching_resume_index, 'To']],
                'Matching_Skills': [best_matching_score]
            })], ignore_index=True)

    print(index_vacancy)


# In[ ]:


result.to_csv('matching_results.csv', index=False)


# In[ ]:


result.to_csv('matching_results1.csv',
              encoding='utf-8',
              index=False)

