.ONESHELL:

init:
	touch local.env

# Container commands

container-django-shell:
	docker compose run --rm --entrypoint bash django

container-run:
	docker compose run --rm --service-ports django
