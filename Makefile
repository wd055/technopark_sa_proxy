.PHONY:

proxy:
	psql -c "\i DB/init.sql;" -U postgres
	python3 main.py

web:
	python3 web_interface.py
