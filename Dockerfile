# База
FROM python:3.12-slim AS base

# Устанавливаем LibreOffice (необходимый для конвертации .docx → .doc)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    libreoffice-writer \
    && rm -rf /var/lib/apt/lists/*

# Создаём рабочий каталог
WORKDIR /app

# Копируем всё приложение
COPY . .

# Устанавливаем зависимости Python (файл находится в app/requirements.txt)
RUN pip install --no-cache-dir -r app/requirements.txt --root-user-action ignore

# фиксируем PYTHONPATH
ENV PYTHONPATH=/app

# Экспонируем порт
EXPOSE 5000

# Запускаем
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app.main:app"]