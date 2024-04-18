FROM python:3.11-slim

ENV PYTHONUNBUFFERED 1
ENV VENV "/venv"
ENV PATH "${VENV}/bin:$PATH"
ENV PYTHONPATH "${PYTHONPATH}:/src"

WORKDIR /src

COPY ./src /src
COPY pyproject.toml poetry.lock ./

RUN apt-get update && apt-get install -y gcc libffi-dev g++
RUN pip install "poetry"
RUN poetry config virtualenvs.create false && \
    poetry install

CMD python app