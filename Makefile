

test:
	./manage.py test tests

requirements:
	pip install -r development.txt

coverage: pyclean
	coverage run manage.py test
	coverage html
	coverage erase
	chromium-browser htmlcov/index.html

pyclean:
	find . -name "*.pyc" -exec rm -rf {} \;
	find . -type d -name "__pycache__" -delete

pip-review:
	pip freeze --local | cut -d = -f 1 | xargs -n 1 pip search | grep -B2 'LATEST:'
