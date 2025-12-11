FROM python:3.11-slim
WORKDIR /app
COPY . /app
RUN apt-get update && apt-get install -y \
    build-essential \
    libcairo2 \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libgdk-pixbuf-2.0-0 \
    libffi-dev \
    shared-mime-info \
    libxml2 \
    libxslt1.1 \
    libjpeg62-turbo \
    libfreetype6 \
    libharfbuzz0b \
    libfribidi0 \
    libthai0 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir -r requirements.txt
ENV PYTHONUNBUFFERED=1
ENV PORT=8000
EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
