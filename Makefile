all:
	python parser.py

tests:
	python fetch-testdata.py
	python tests.py
