
build:
	docker build -t pokeapi-frontend -f ./docker/frontend/Dockerfile-frontend .
	docker build -t pokeapi-app -f ./docker/app/Dockerfile-app .
	docker image prune -f
