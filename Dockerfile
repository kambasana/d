FROM node:24-slim AS world-explorer-ui
WORKDIR /build
COPY apps/world-explorer/package.json apps/world-explorer/package-lock.json ./
RUN npm ci
COPY apps/world-explorer/ ./
RUN npm run build

FROM python:3.12-slim
WORKDIR /workspace
COPY pyproject.toml requirements-dev.txt ./
RUN pip install --no-cache-dir -r requirements-dev.txt
COPY . .
COPY --from=world-explorer-ui /build/dist /workspace/apps/world-explorer/dist
ENTRYPOINT ["python", "scripts/entrypoint.py"]
CMD ["validate"]
