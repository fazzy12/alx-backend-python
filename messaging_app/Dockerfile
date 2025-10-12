# official Python 3.10 image as the base layer
FROM python:3.10

# working directory
WORKDIR /app

COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

EXPOSE 8000 
#"-p"

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
