FROM python:3.8-slim

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

EXPOSE 3000
ENV product=https://waexur8syl.execute-api.eu-central-1.amazonaws.com/prod/products
ENV cart=http://naxa777-cart-api-demo.eu-central-1.elasticbeanstalk.com

CMD ["gunicorn", "-b", "0.0.0.0:3000", "app:app"]