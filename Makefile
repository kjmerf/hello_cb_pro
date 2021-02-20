test:
	python3 -m unittest discover;

main:
	docker-compose build main;
	docker-compose run main;