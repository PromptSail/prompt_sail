FROM python:3.10.2-slim-buster AS requirements

ADD pyproject.toml poetry.lock ./

RUN apt-get update && apt-get install -y curl && \
    curl -sSL https://install.python-poetry.org | python3 -

# just to create virtualenv, maybe there is a better way
RUN /root/.local/bin/poetry export -f requirements.txt > /dev/null

RUN /root/.local/bin/poetry export -f requirements.txt --without-hashes > req.txt && \
    sed 's/-e //' req.txt > requirements.txt && \
    sort requirements.txt > production.txt

RUN /root/.local/bin/poetry export -f requirements.txt --with dev --without-hashes > req.txt && \
    sed 's/-e //' req.txt > requirements.txt && \
    sort requirements.txt > all.txt

# We need only development dependencies in development.txt (without production requirements)
RUN comm -3 production.txt all.txt > development.txt

FROM python:3.10.2 AS base
ENV PYTHONUNBUFFERED 1

WORKDIR /src
COPY --from=requirements production.txt ./
RUN apt-get update && rm -rf /var/lib/apt/lists/* && \
    useradd -u 1000 promptsail && \
    chown -R promptsail /src && \
    pip install --no-cache --no-cache-dir -r ./production.txt

COPY src/. /src
COPY static/. /static

FROM base as production
USER promptsail
CMD uvicorn app:app --proxy-headers --host 0.0.0.0 --port=${PORT:-8000}


