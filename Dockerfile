# Используем более конкретную версию базового образа Python
FROM python:3.11-slim-buster

# Устанавливаем переменную окружения PYTHONUNBUFFERED для вывода
# вывода Python в реальном времени без буферизации
ENV PYTHONUNBUFFERED=1

WORKDIR /usr/src/app

# Обновляем пакетный менеджер и устанавливаем зависимости
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Клонируем репозиторий из GitHub в текущую директорию
RUN git clone https://github.com/kizimenko/streamlit_ab_template.git 

WORKDIR /usr/src/app/streamlit_ab_template/app

# Устанавливаем зависимости Python из файла requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Открываем порт 8501 для доступа к серверу Streamlit
EXPOSE 8501

# Устанавливаем проверку состояния контейнера с помощью команды curl
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# Запускаем приложение Streamlit при запуске контейнера
CMD ["streamlit", "run", "streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
