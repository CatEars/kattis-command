init:
	virtualenv venv -p python3
	( \
		. ./venv/bin/activate; \
		pip install -r requirements.txt; \
	)


install:
	. ./venv/bin/activate; \
	pip install --upgrade .; \


test:
	. ./venv/bin/activate; \
	pytest test; \


.PHONY: init install test
