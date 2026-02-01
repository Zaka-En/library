FROM node:20-alpine AS builder

WORKDIR /app

RUN corepack enable && corepack prepare pnpm@latest --activate

# Copiar todos los archivos primero, incluyendo la estructura completa
COPY . .

# Instalar todas las dependencias (incluyendo devDependencies)
ENV CI=true
RUN pnpm install --frozen-lockfile

# Ahora hacer el build
RUN pnpm run build

FROM node:20-alpine

WORKDIR /app

RUN corepack enable && corepack prepare pnpm@latest --activate

COPY --from=builder /app/build build/
COPY --from=builder /app/package.json .
COPY --from=builder /app/pnpm-lock.yaml .
ENV CI=true
RUN pnpm install --prod --frozen-lockfile

EXPOSE 3000

CMD ["node", "build"]