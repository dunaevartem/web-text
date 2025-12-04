# База
FROM python:3.12-slim AS base

# Устанавливаем LibreOffice (необходимый для конвертации .docx → .doc)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    libreoffice-writer \
    && rm -rf /var/lib/apt/lists/*

# Создаём рабочий каталог
WORKDIR /app

# Копируем требования и устанавливаем
COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем всё приложение
COPY app /app/app

# Копируем все тесты
COPY tests /app/tests

# Экспонируем порт
EXPOSE 5000

# Запускаем
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app.main:app"]