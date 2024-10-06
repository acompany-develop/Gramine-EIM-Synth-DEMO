run:
	mkdir -p .logs
	docker compose down -v
	docker compose up --build | tee .logs/$(shell date +'%y%m%d%H%M').log

stop:
	docker-compose down -v
