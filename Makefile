init:
	virtualenv venv -p python3
	. ./venv/bin/activate; \
	pip install -r requirements.txt


install:
	. ./venv/bin/activate; \
	pip install --upgrade .; \


test:
	. ./venv/bin/activate; \
	pytest test -m "not submission"; \


testall:
	. ./venv/bin/activate; \
	pytest test -v; \


.PHONY: init install test testall
