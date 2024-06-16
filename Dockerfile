FROM python:3.11

WORKDIR /app

RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/opt/poetry python3 -
ENV PATH = "${PATH}:/opt/poetry/bin"
COPY atomic_sovus atomic_sovus
COPY ./poetry.lock ./pyproject.toml .
RUN poetry config virtualenvs.create false && poetry install --without dev

COPY scripts scripts
RUN ["python3", "scripts/download_models.py"]

COPY vectorstores vectorstores
COPY data data
COPY ./app.py .
COPY pages pages

EXPOSE 8501
CMD ["streamlit", "run", "app.py"]
