FROM python:3.11

WORKDIR /app

RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/opt/poetry python3 -
ENV PATH = "${PATH}:/opt/poetry/bin"
COPY ./poetry.lock ./pyproject.toml .
RUN poetry config virtualenvs.create false && poetry install --without dev

COPY scripts scripts
RUN ["python3", "scripts/download_models.py"]

COPY atomic_sovus atomic_sovus
COPY vectorstores vectorstores
COPY ./app.py .
COPY ./.env .

EXPOSE 8501
CMD ["streamlit", "run", "app.py"]
