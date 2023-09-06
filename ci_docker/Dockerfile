
FROM python:3.10-slim as builder

RUN mkdir -p /opt/app/

WORKDIR /home/opt/ 

COPY index.py poetry.lock pyproject.toml app/
COPY app/ app/app/
COPY app/assets/ app/assets/

WORKDIR /home/opt/app/

# SPACE to run Deployment specific poetry commands for config other packages
# RUN --mount=type=secret, id=any_PYPI_URL --mount=type=secret, id=any_PYPI_TOKEN \
# pip install poetry==1.4.2 --no-cache-dir && \
# export PATH="$(PATH)":"$(HOME)"/.local/bin && \
# poetry config virtualenvs.create true

RUN poetry install --only main



# working layer


FROM python:3.10-slim

WORKDIR /opt/app/

RUN pip install --upgrade pip

COPY --from=builder /home/opt/app/ /home/opt/app/
ENV PATH=/home/opt/app/.venv/bin:$PATH
ENV PYTHONUNBUFFERED 1

WORKDIR /home/opt/app/

CMD ["guicorn", "-b", "0.0.0.0:8050", "index:server", "-aaccess-logfile", "-", "--limit-request-fields", "300", "--limit-request-field_size", "10000", "--timeout", "60"]




