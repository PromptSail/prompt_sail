FROM python:3.10.2-slim-buster AS base

ENV PYTHONUNBUFFERED=1 \
    POETRY_VERSION=1.1.13 
    
WORKDIR /src    

# Install curl and Poetry in a single step, and clean up the apt cache to keep the image small
RUN apt-get update && apt-get install -y --no-install-recommends curl \
    && curl -sSL https://install.python-poetry.org | python3 - \
    && ln -s /root/.local/bin/poetry /usr/local/bin/poetry \
    && apt-get purge -y --auto-remove curl \
    && rm -rf /var/lib/apt/lists/*

# Copy the Python dependency files into the image
COPY pyproject.toml poetry.lock ./

# Create the virtual environment and export the dependency lists
RUN poetry config virtualenvs.create false \
    && poetry install --no-dev --no-interaction --no-ansi \
    && poetry export -f requirements.txt --without-hashes --output production.txt \
    && poetry export -f requirements.txt --dev --without-hashes --output all.txt \
    && comm -23 all.txt production.txt > development.txt

# Set up a non-root user for security purposes
RUN useradd --create-home promptsail

# Ensure the user has access to the workdir
RUN chown -R promptsail /src

# Switch to non-root user
USER promptsail

# Copy only the necessary files for running the application
COPY --chown=promptsail src/ /src/
COPY --chown=promptsail static/ /static/

# Continue as new stage to minimize production image size
FROM base as production

# ARGs are only available in the build stage they were declared in, so re-declare BUILD_SHA here
ARG BUILD_SHA

# Set build SHA environment variable
ENV BUILD_SHA=${BUILD_SHA}

# Copy the production requirements and install them
COPY --from=base --chown=promptsail /src/production.txt ./
RUN pip install --no-cache-dir -r production.txt

# Expose the port the app runs on
EXPOSE 8000

# Run the application
CMD uvicorn app:app --proxy-headers --host 0.0.0.0 --port=${PORT:-8000}



#FROM python:3.10.2-slim-buster AS requirements
#ARG BUILD_SHA
#
#ADD pyproject.toml poetry.lock ./
#
#RUN apt-get update && apt-get install -y curl && \
#    curl -sSL https://install.python-poetry.org | python3 -
#
## just to create virtualenv, maybe there is a better way
#RUN /root/.local/bin/poetry export -f requirements.txt > /dev/null
#
#RUN /root/.local/bin/poetry export -f requirements.txt --without-hashes > req.txt && \
#    sed 's/-e //' req.txt > requirements.txt && \
#    sort requirements.txt > production.txt
#
#RUN /root/.local/bin/poetry export -f requirements.txt --with dev --without-hashes > req.txt && \
#    sed 's/-e //' req.txt > requirements.txt && \
#    sort requirements.txt > all.txt
#
## We need only development dependencies in development.txt (without production requirements)
#RUN comm -3 production.txt all.txt > development.txt
#
#FROM python:3.10.2 AS base
#ENV PYTHONUNBUFFERED 1
#WORKDIR /src
#COPY --from=requirements production.txt ./
#RUN apt-get update && rm -rf /var/lib/apt/lists/* && \
#    useradd -u 1000 promptsail && \
#    chown -R promptsail /src && \
#    pip install --no-cache --no-cache-dir -r ./production.txt
#
#COPY src/. /src
#COPY static/. /static
#
#FROM base as production
#ENV BUILD_SHA=${BUILD_SHA}
#USER promptsail
#CMD uvicorn app:app --proxy-headers --host 0.0.0.0 --port=${PORT:-8000}


