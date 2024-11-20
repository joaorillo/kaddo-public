# Simplify manage.py commands
MANAGE = docker-compose exec api python manage.py
.PHONY: manage
manage:
	$(MANAGE) $(filter-out $@,$(MAKECMDGOALS))
