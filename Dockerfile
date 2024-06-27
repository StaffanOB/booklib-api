FROM python:3.10
EXPOSE 5000
WORKDIR /app
ENV FLASK_APP=app.py:app
COPY requirements.txt .

RUN pip install --no-cache-dir --upgrade -r requirements.txt
COPY . .
CMD ["/bin/bash", "docker-entry-point.sh"]

