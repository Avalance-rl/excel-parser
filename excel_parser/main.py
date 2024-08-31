import json
import pandas as pd
import re



def replaceTextOfType(s: str) -> str:
    comparassion = s.upper()
    if comparassion == "ТЕКСТОВЫЙ":
        return "text"
    if comparassion == "ОДИН ВАРИАНТ ОТВЕТА":
        return "select"
    if comparassion == "НЕСКОЛЬКО ВАРИАНТОВ ОТВЕТА":
        return "multiselect"


def answersHandler(s):
    if pd.isna(s):
        return []
    pattern = r'\d+\)\s*'
    parts = re.split(pattern, s)
    options = [part.strip() for part in parts[1:] if part.strip()]

    return options

def rightAnswersHandler(s: str):
    correct_answers_list = [answer.strip() for answer in s.split(',')]

    return correct_answers_list


dataframe1 = pd.read_excel('Events Bot for Freshmen.xls', sheet_name='Мероприятия')
dataframe2 = pd.read_excel('Events Bot for Freshmen.xls', sheet_name='Вопросы')

events1 = dataframe1[dataframe1.columns[0]]
events2 = dataframe2[dataframe2.columns[0]]
united_data = []

for i in range(len(events1)):
    data = {
        "name": events1[i],
        "description": dataframe1[dataframe1.columns[1]][i],
        "type": dataframe1[dataframe1.columns[2]][i],
        "guest_count": dataframe1[dataframe1.columns[3]][i],
        "coast": 10,
        "interval": 30,         
    }
    questions = []
    for j in range(len(events2)):
        if events2[j] == events1[i]:
            questions.append(
                {
                    "text": dataframe2[dataframe2.columns[1]][j],
                    "type": replaceTextOfType(dataframe2[dataframe2.columns[2]][j]),
                    "answers": answersHandler(dataframe2[dataframe2.columns[3]][j]),
                    "right_answers": rightAnswersHandler(str(dataframe2[dataframe2.columns[4]][j])) 
                }
            )
    data.update({
        "questions": questions
    })
    united_data.append(data)


for index, item in enumerate(united_data):
    filename = f"Тест_{index + 1}.json"
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(item, file, ensure_ascii=False, indent=4)

print("JSON files have been created successfully.")
