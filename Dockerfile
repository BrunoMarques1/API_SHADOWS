FROM python:3.7

RUN pip install fastapi uvicorn sqlalchemy pydantic pymysql python-dotenv

EXPOSE 8000

COPY . /app
COPY .env /app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]