FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY src/* /app/
EXPOSE 8000
ENTRYPOINT [ "uvicorn", "--host", "0.0.0.0", "--port", "8000", "api:app" ]
RUN pytest test_api.py -v
# Ändrat från 8080 till 8000 på både ENTRYPOINT och EXPOSE
# Lagt till Run pytest test_api.py -v