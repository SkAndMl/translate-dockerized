FROM python:3.10.14-slim-bullseye

# set workdir
WORKDIR /app

# copy lib requirements and install them
COPY requirements.txt .
RUN pip install -r requirements.txt

# copy test and api code
COPY ./config.json .
COPY ./main.py .
COPY ./download_model.py .
COPY ./test.py .
COPY ./data ./data

# copy 'sh' scripts, change their access and run it
COPY ./download_model.sh .
COPY ./run_test.sh .
RUN chmod +x ./download_model.sh
RUN chmod +x ./run_test.sh
RUN ./download_model.sh
RUN ./run_test.sh

# expose port
EXPOSE 8000

# default command for the container
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]