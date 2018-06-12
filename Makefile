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

down: ## Stop containers
	docker-compose stop

remove: ## Rmove all containers
	docker-compose down

test: ## Run tests inside stoodi project
	docker-compose exec app python manage.py test

restart: ## Restart all containers
	docker-compose restart

logs: ## Run tests inside stoodi project
	docker-compose logs -f --tail=100

.DEFAULT_GOAL := help
