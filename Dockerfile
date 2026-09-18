FROM python:3.11-slim
WORKDIR /usr/src/app
COPY modular_auditor.py .
CMD ["python", "modular_auditor.py"]