FROM python:3.12-slim
RUN pip install --no-cache-dir pytest==8.* httpx==0.27.*
WORKDIR /tests
CMD ["pytest", "-q", "/tests"]
