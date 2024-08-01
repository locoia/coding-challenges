VENV := .venv

rm_venv:
	source deactivate || true
	rm -rf $(VENV)

$(VENV): rm_venv
	command -v deactivate && source deactivate || true
	python -m venv $(VENV)
	source $(VENV)/bin/activate && pip install --upgrade pipx pip-tools

setup:
	test -r $(VENV) || make $(VENV)
	source $(VENV)/bin/activate && pipx install poetry \
	&& poetry install --no-root

runlocal:
	$(VENV)/bin/flask --app gistapi/gistapi.py run

rundocker:
	docker build --no-cache -t backend-coding-challenge .
	docker run -it -p 5001:5000 backend-coding-challenge

runchecks:
	$(VENV)/bin/python -m black gistapi/gistapi.py
	$(VENV)/bin/python -m flake8 gistapi/gistapi.py

runtests:
	$(VENV)/bin/python -m unittest discover tests
