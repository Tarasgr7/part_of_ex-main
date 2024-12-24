FROM python:3.11

WORKDIR /vpn_servise

COPY requirements.txt /vpn_servise/

RUN pip install --no-cache-dir -r requirements.txt

COPY . /vpn_service/

EXPOSE 8080

CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8080"]