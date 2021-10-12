build-env:
	docker build -t orangenal/roombot-env:latest EnvImage/

install:
	docker build -t bot .
	docker run --mount type=volume,source=bot-vol,destination=/app/volume --name bot-cont bot

install-v:
	docker volume create bot-vol
	docker build -t bot .
	docker run --mount type=volume,source=bot-vol,destination=/app/volume --name bot-cont bot

clear:
	docker container prune
	docker image rm bot

run:
	docker run --mount type=volume,source=bot-vol,destination=/app/volume --name bot-cont bot

reinstall:
	docker container prune
	docker image rm bot
	docker build -t bot .
	docker run --mount type=volume,source=bot-vol,destination=/app/volume --name bot-cont bot