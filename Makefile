
build:
	docker build -t pokeapi-frontend -f ./docker/frontend/Dockerfile-frontend .
	docker build -t danil7/pokeapi -f ./docker/app/Dockerfile-app .
	docker image prune -f
