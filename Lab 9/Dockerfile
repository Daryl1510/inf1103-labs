FROM python:3.12-slim
WORKDIR /app
COPY *.py .
COPY products.csv .
COPY tests/ tests/
CMD ["python", "inventory_manager.py"]
