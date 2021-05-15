.PHONY: all
all: food.csv

food.csv:
	curl https://corgis-edu.github.io/corgis/datasets/csv/food/food.csv > food.csv

ipy/bin/python:
	python3 -m venv ipy
	source ipy/bin/activate && pip install -r requirements.txt