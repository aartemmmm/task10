FROM python:3.12-slim

COPY release/*.whl /tmp/shop/
RUN pip install --no-cache-dir --no-deps /tmp/shop/*.whl && rm -rf /tmp/shop

USER 65532:65532
EXPOSE 8080
HEALTHCHECK --interval=5s --timeout=3s --start-period=5s --retries=3 \
  CMD ["python", "-c", "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8080/health', timeout=2).close()"]
CMD ["python", "-m", "seminar_shop", "--host", "0.0.0.0"]
