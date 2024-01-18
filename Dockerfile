FROM python:3.10-alpine3.18
LABEL authors="deyakk"

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /todo

COPY requirements.txt /todo/requirements.txt

COPY src ./src

COPY .env .

RUN pip install -r requirements.txt

RUN rm -rf requirements.txt

EXPOSE 80

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]