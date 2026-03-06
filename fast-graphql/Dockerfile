# FROM python:3.13-alpine as builder

# # install UV
# COPY --from=ghcr.io/astral-sh/uv:0.9.29 /uv /bin/uv

# COPY . /app/

# WORKDIR /app
# RUN --mount=type=cache,target=/root/.cache/uv \
#   uv sync --no-dev --frozen

# FROM python:3.12-alpine

# COPY --from=build /app/.venv /app/.venv
# COPY . /app/

# WORKDIR 

# EXPOSE 8000

# CMD ["uvicorn", "app.app:app", "--host", "0.0.0.0", "--port", "8000"]


FROM python:3.13-slim

# install UV
COPY --from=ghcr.io/astral-sh/uv:0.4.3 /uv /bin/uv

# copy files
COPY pyproject.toml uv.lock /app/

WORKDIR /app
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen

COPY . /app/

CMD ["uv", "run", "python", "-m" , "app"]