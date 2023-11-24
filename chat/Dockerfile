ARG FUNCTION_DIR="/chat/app"


# Include global arg in this stage of the build
ARG FUNCTION_DIR

# Setup base environment variables 
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    LANG=C.UTF-8 \
    LC_ALL=C.UTF-8

# Copy contract package from the base image at the root of the project. 
COPY --chown=app ${FUNCTION_DIR}

# Set work directory
WORKDIR ${FUNCTION_DIR}

# Install pipenv and dependencies
RUN PIPENV_VENV_IN_PROJECT=1 pipenv install --deploy --clear


# Include global arg in this stage of the build
ARG FUNCTION_DIR

WORKDIR ${FUNCTION_DIR}

# Copy files from python-deps to runtime image.
# NOTE: Copy entire directory to accomodate for "editable" installation of the ai package
COPY --from=python-deps --chown= ${FUNCTION_DIR} ${FUNCTION_DIR}

# Set user for running the application
USER

ENV PATH="${FUNCTION_DIR}/.venv/bin:$PATH"

CMD ["streamlit", "run", "src/main.py"]
