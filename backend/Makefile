install:
	pip install -r requirements.txt


dev:
	uvicorn src.config.asgi:app --reload --host 0.0.0.0 --port 8000


prod:
	uvicorn src.config.asgi:app --host 0.0.0.0 --port 8000 --workers 4


migrate:
	python manage.py migrate


makemigrations:
	python manage.py makemigrations
