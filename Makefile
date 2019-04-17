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

dockerbuild:
	docker build . -t kattis-cmd-testimage

dockertest:
	make dockerbuild
	docker run "kattis-cmd-testimage"
