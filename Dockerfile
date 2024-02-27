ARG PYTHON_VERSION=3.11
FROM python:${PYTHON_VERSION}-bullseye
LABEL maintainer="Dr. Jahed Naghipoor"

WORKDIR /app
COPY requirements.txt setup.py ./
RUN pip install -r requirements.txt --no-cache-dir --prefer-binary
COPY ./src ./src
COPY README.md ./
RUN pip install .

ENTRYPOINT ["python", "-OO", "-m", "ml_devops_dida_task"]
