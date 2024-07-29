FROM python:3.10.14-slim-bullseye
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY main.py .
COPY test.py .
COPY data ./data
RUN python test.py
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]