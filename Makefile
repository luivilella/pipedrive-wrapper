all:
	@echo "Hello $(LOGNAME), nothing to do by default"
	@echo "Try 'make help'"

help: ## This help.
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

build: ## Build images and run the containers
	cp app/.env.template app/.env
	vi app/.env
	cp docker/nginx/nginx.conf.template docker/nginx/nginx.conf
	vi docker/nginx/nginx.conf
	docker-compose build
	docker-compose up -d

up: ## Start containers and run the project in dev mode
	docker-compose start
	docker-compose exec assets yarn build:prod
	docker-compose exec app uwsgi --socket 0.0.0.0:8080 --workers 4 --protocol=http -w wsgi

up-debug: ## Start containers and debug the project in dev mode
	docker-compose start
	docker-compose exec assets yarn build
	docker-compose exec app python wsgi.py

assets-watch:
	docker-compose start
	docker-compose exec assets yarn build:watch

down: ## Stop containers
	docker-compose stop

remove: ## Rmove all containers
	docker-compose down

test: ## Run tests inside
	docker-compose exec app pytest

restart: ## Restart all containers
	docker-compose restart

logs: ## Run tests inside
	docker-compose logs -f --tail=100

cmd: ## Run a command line inside
	docker-compose exec app /bin/bash

.DEFAULT_GOAL := help
