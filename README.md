
Сборка и запуск
```bash
docker build -t visit-analyzer:base .
docker compose up -d
docker exec visit_analyzer_app apt update
docker exec visit_analyzer_app apt install -y ffmpeg
docker exec ollama ollama run llama3.1
```

Тестовые запросы

curl -sS -X POST http://localhost:8080/v1/visit/analyze \
  -H "Accept: application/json" \
  -F "audio=@test-doctor.mp3" \
  -F "lang=ru" | jq .


curl -sS -X POST http://localhost:8080/v1/visit/analyze-transcript \
-H "Content-Type: application/json" \
-d '[
    {
      "start": 0.5,
      "end": 3.2,
      "speaker": "SPEAKER_01",
      "text": "Здравствуйте, меня зовут доктор Иванов. Как к вам можно обращаться?"
    },
    {
      "start": 3.3,
      "end": 6.0,
      "speaker": "SPEAKER_00",
      "text": "Добрый день, я Мария."
    },
    {
      "start": 6.5,
      "end": 15.0,
      "speaker": "SPEAKER_01",
      "text": "Мария, расскажите, что вас беспокоит?"
    },
    {
      "start": 15.1,
      "end": 25.0,
      "speaker": "SPEAKER_00",
      "text": "У меня последние дни часто болит голова и немного повышается давление."
    },
    {
      "start": 25.5,
      "end": 35.0,
      "speaker": "SPEAKER_01",
      "text": "Понятно. Есть ли у вас хронические заболевания или принимаете ли вы какие-то лекарства?"
    },
    {
      "start": 35.2,
      "end": 42.0,
      "speaker": "SPEAKER_00",
      "text": "Да, у меня гипертония, пью амлодипин."
    },
    {
      "start": 45.0,
      "end": 52.0,
      "speaker": "SPEAKER_01",
      "text": "Давление сейчас 150 на 95, пульс 80. Рост у вас 165 см, вес 70 кг."
    },
    {
      "start": 55.0,
      "end": 65.0,
      "speaker": "SPEAKER_01",
      "text": "Предварительный диагноз — артериальная гипертензия. Рекомендую продолжать терапию и проконсультироваться у кардиолога."
    },
    {
      "start": 66.0,
      "end": 70.0,
      "speaker": "SPEAKER_01",
      "text": "Спасибо за визит, до свидания."
    },
    {
      "start": 70.5,
      "end": 72.0,
      "speaker": "SPEAKER_00",
      "text": "До свидания."
    }
  ]' | jq .
