# Make targets for CDA


mongo:
	docker-compose up -d

test:
	pytest