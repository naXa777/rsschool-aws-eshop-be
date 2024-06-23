# rsschool-aws-eshop-be

go to main directory
```sh
cd src/product-service
```

install dependencies
```sh
pip install -r .\requirements.txt
```

run unit tests
```sh
python -m pytest
```

deploy to AWS
```sh
cdk deploy --all
```

populate database with sample data (do it once!)
```sh
cd resources
python populate_db.py
```
