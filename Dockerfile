FROM python:3.12-slim
WORKDIR /workspace
COPY pyproject.toml requirements-dev.txt ./
RUN pip install --no-cache-dir -r requirements-dev.txt
COPY . .
ENTRYPOINT ["python", "scripts/entrypoint.py"]
CMD ["validate"]
