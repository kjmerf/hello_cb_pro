test:
	python3 -m unittest discover;

main:
	docker-compose up --build --remove-orphans main
