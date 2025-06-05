FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y libpq-dev && pip install --upgrade pip

COPY pyproject.toml poetry.lock* ./
RUN pip install poetry && poetry config virtualenvs.create false && poetry install

COPY . .

EXPOSE 8000
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
