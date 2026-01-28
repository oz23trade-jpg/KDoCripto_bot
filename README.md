# K DoCripto Bot

Telegram-бот для обучения крипте с рефералкой, квизами, лотереей и Telegram Stars.

## Запуск локально

1. Склонируй репозиторий
2. Создай .env по примеру выше
3. Подними БД (Supabase или локальный Postgres)
4. Выполни SQL-схему из документации

### Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload