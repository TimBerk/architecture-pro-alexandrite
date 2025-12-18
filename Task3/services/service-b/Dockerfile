FROM python:3.12-slim

WORKDIR /app

RUN pip install --no-cache-dir uv
COPY pyproject.toml uv.lock /app/
RUN uv sync --frozen --no-dev

COPY app.py /app/

EXPOSE 8080

CMD ["uv", "run", "flask", "run", "--port", "8080", "--host", "0.0.0.0"]
