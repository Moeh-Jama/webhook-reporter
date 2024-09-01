FROM python:3.9-slim

ENV COVERAGE_FILE=${INPUT_COVERAGE_FILE}
ENV FRAMEWORK=${INPUT_FRAMEWORK}
ENV PROVIDER=${INPUT_PROVIDER}
ENV TEST_RESULTS=${INPUT_TEST_RESULTS}
ENV WEBHOOK_URL=${INPUT_WEBHOOK_URL}

COPY . /app
WORKDIR /app

RUN pip install --no-cache-dir -r requirements.txt


# Set the entry point to your Python script
ENTRYPOINT ["python", "/app/main.py"]
