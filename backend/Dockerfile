FROM python:3.11-slim AS builder
WORKDIR /backend
COPY requirements.txt .
run --mount=type=cache,target=/root/.cache/pip \
    pip install -r ./requirements.txt

FROM python:3.11-slim
WORKDIR /backend
ENV PATH="/venv/bin:$PATH"

COPY . .

EXPOSE 8080

CMD ["/venv/bin/python3", "-m", "uvicorn", "main:'tracky'", "--host=0.0.0.0", "--port=8080"]