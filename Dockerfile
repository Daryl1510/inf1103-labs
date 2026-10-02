FROM python:3.12-slim
WORKDIR /app
COPY inventory_manager.py .
CMD ["python", "inventory_manager.py"]