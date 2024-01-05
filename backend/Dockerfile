FROM python:3.10.2-slim-buster AS base

ENV PYTHONUNBUFFERED=1 \
    POETRY_VERSION=1.1.13 
    
WORKDIR /src    

# Install curl and Poetry in a single step, and clean up the apt cache to keep the image small
RUN apt-get update && apt-get install -y --no-install-recommends curl \
    && curl -sSL https://install.python-poetry.org | python3 - --version 1.7.1 \
    && ln -s /root/.local/bin/poetry /usr/local/bin/poetry \
    && apt-get purge -y --auto-remove curl \
    && rm -rf /var/lib/apt/lists/*


# Copy the Python dependency files into the image
COPY pyproject.toml ./
RUN poetry lock

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
COPY --chown=promptsail src /src/
COPY --chown=promptsail static /static/

# Continue as new stage to minimize production image size
FROM base as production

# ARGs are only available in the build stage they were declared in, so re-declare BUILD_SHA here
ARG BUILD_SHA

# Set build SHA environment variable
ENV BUILD_SHA=${BUILD_SHA}

# Copy the production requirements and install them
COPY --from=base --chown=promptsail src/production.txt ./
RUN pip install --no-cache-dir -r production.txt

# Expose the port the app runs on
EXPOSE 8000

# Run the application
CMD uvicorn app:app --proxy-headers --host 0.0.0.0 --port=${PORT:-8000}