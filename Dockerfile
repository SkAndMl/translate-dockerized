FROM python:3.10.14-slim-bullseye
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY ./config.json .
COPY ./main.py .
COPY ./download_model.py .
COPY ./test.py .
COPY ./data ./data
COPY ./download_model.sh .
COPY ./run_test.sh .
RUN chmod +x ./download_model.sh
RUN chmod +x ./run_test.sh
RUN ./download_model.sh
RUN ./run_test.sh
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]