FROM python:3.14

WORKDIR /code

ENV PYTHONUNBUFFERED=1

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./App /code/App

EXPOSE 8501

CMD [ "streamlit", "run", "./App/frontend.py"]
