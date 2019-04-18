# PracticeSurveys

# Необходимые компоненты:
```python 
pip install pandas
pip install plotly
pip install dash-daq
pip install dash
pip install dash-core-components
pip install dash-html-components
```

# Запуск программы
## Вариант 1 (с ручной загрузкой файла):
1. Загрузить файл с результатами анкетирования в папку **surveys**. Файл должен иметь имя расширение **.csv** **Внимание!** В  папке должен лежать только один файл с этим расширением. Имя файла должно быть написано латиницей, при наименовании кириллицей возникает ошибка.
2. Запустить программу:
```python 
python main.py
```
3. Открыть в браузере: http://localhost:8050/

## Вариант 2 (с загрузкой файла из облака Google Drive):
1. Задать идентификатор файла **docId** и флаг загрузки **isFileNeedToBeDownloaded=True** в программном файле **main.py**. Файл из облака должен иметь публичный доступ. (После загрузки файла флагу надо опять задать значение **False**).
2. При необходимости установить библиотеку для работы с облаком:
```python 
pip install googledrivedownloader
```
3. Запустить программу:
```python 
python main.py
```
4. Открыть в браузере: http://localhost:8050/

# Важные примечания
В программе задано значение **0,25** для отклонения среднего значения, для расчета релевантности данных, его можено изменить, задав в файле программы **main.py** новое значение **avgErr**

# Как можно обновить файл
Удалить старый файл из папки **surveys** и положить туда новый или выполнить загрузку из облака, описанную в **Варианте 2**.

# Что делать если изменилась структура анкеты
В папке **dataPreparation** изменить правила именования полей в программе **dataPreparation.py**.

Поля следует именовать следующим образом: 
Все оценочные поля должны начинаться со слова **оценка**, для них применяется:
* рассчет среднего значения
* рассчет релевантности выборки для подсчета среднего значения
* построение диаграммы размаха
* построения графиков рассеяния

Все текстовые поля должны начинаться со слова **мнение**, для них применяется:
* извлечение тем из корпуса текстов в рамках одинаковых полей на каждом курсе
* визуализация тем и всех сообщений в виде таблиц

**Внимание!** Помимо полей начинающихся со слова "мнение" в текстовые поля добавляется поле с именем **предложения**, в случае, если это поле было убрано, его надо убрать из кода (программа **main.py** строка **58**). Программа отлавливает только одно поле с таким названием.
