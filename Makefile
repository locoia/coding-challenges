run:
	docker-compose -f docker-compose.yaml up -d --build

stop:
	docker-compose -f docker-compose.yaml down

test:
	docker-compose -f docker-compose.yaml run --rm backend sh -c "pytest tests -vv && flake8 gistapi tests"