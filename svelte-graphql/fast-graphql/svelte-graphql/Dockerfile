# Ha tardado 60 segundos

FROM node:24-slim AS base
ENV PNPM_HOME="/pnpm"
ENV PATH="$PNPM_HOME:$PATH"
RUN corepack enable

#============

FROM base AS build
WORKDIR /app

COPY package.json pnpm-lock.yaml pnpm-workspace.yaml ./
COPY ./svelte-graphql/package.json ./svelte-graphql/
COPY ./comp-library/package.json ./comp-library/
RUN --mount=type=cache,id=pnpm,target=/pnpm/store pnpm install --frozen-lockfile

COPY . .

RUN pnpm run -r build
RUN pnpm deploy --prod --filter=svelte-graphql /prod/app

#============

FROM base AS app1
ENV NODE_ENV=production
COPY --from=build /prod/app /prod/app
COPY --from=build /app/svelte-graphql/build /prod/app/build
WORKDIR /prod/app
EXPOSE 3000
CMD node build/index.js
