SRC=achilles

test:
	DJANGO_SETTINGS_MODULE=test_settings python setup.py nosetests

pep8:
	pep8 $(SRC)

pyflakes:
	pyflakes $(SRC)
