# chat-recap
Chat Recap — инструмент для анализа чатов, который обрабатывает историю сообщений и предоставляет детальную статистику по переписке.

## Содержание
- [Возможности](#возможности)
- [Описание решения](#описание-решения)
- [Использование](#использование)
- [Пример работы](#пример-работы)
- [TODO](#todo)

---

## Возможности
- Подсчет количества сообщений каждого собеседника
- Анализ наиболее часто используемых слов
- Подсчет количества эмодзи и определение самых популярных
- Вычисление среднего времени ответа
- Поиск наиболее активного периода общения

---

## Описание решения
Проект обрабатывает JSON-файл с историей сообщений, анализируя тексты на основе регулярных выражений. Он вычисляет статистику по количеству сообщений, среднему времени ответа, самым популярным словам и эмодзи. 

Используется объектно-ориентированный подход: ChatAnalyzer управляет всей логикой анализа, а входные данные загружаются через data_loader.py. Результаты выводятся в консоль.

---

## Использование
1.  Установка зависимостей
    
    pip install -r requirements.txt
    
2. Подготовьте JSON-файл с историей чатов (выгрузить его можно в приложении Telegram на ПК, пример в `result.json`).
3. Запустите анализ:
   
   python main.py
   
4. Получите статистику в консоли.

## Пример работы
Программа выводит результаты анализа в понятном формате:
```
chatter: Alice
total messages: 50
most used words:
Bob: [('reply', 17), ('example', 14), ('message', 12), ('about', 1)]
Alice: [('reply', 18), ('example', 14), ('message', 11)]
messages sent:
Bob: 25
Alice: 25
avg response times (s):
Bob: 312.0
Alice: 300.0
most used emojis:
Bob: [('🍕', 2), ('🌟', 1), ('😄', 1)]
Alice: [('😄', 3), ('🎶', 2)]
most active month: from 2023-04-30 to 2023-05-29 with msg count of 50
```
---

## TODO:
- [ ] Добавление новых метрик
- [ ] Визуализация данных с помощью графиков
- [ ] Генерация красивых итоговых изображений