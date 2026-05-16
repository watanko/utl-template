FROM node:26-bookworm-slim AS runtime

WORKDIR /workspace/frontend

ENV COREPACK_ENABLE_DOWNLOAD_PROMPT=0

COPY frontend/package.json frontend/pnpm-lock.yaml ./
RUN corepack enable && corepack pnpm install --frozen-lockfile

COPY frontend/index.html ./index.html
COPY frontend/biome.json frontend/tsconfig.json ./
COPY frontend/src ./src

EXPOSE 5173

CMD ["corepack", "pnpm", "dev", "--host", "0.0.0.0", "--port", "5173"]
