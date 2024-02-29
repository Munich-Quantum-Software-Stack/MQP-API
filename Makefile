$(eval VERSION=$(shell grep -m 1 version pyproject.toml | tr -d '"' | cut -d' ' -f3 | tr -s ' ' | tr -d "'" ) )

DOCKERHUB=dockerhub.quantum.lrz.de

build-image:
	docker build --no-cache -t bqp-api -t bqp-api:${VERSION} --build-arg PYTHONUNBUFFERED="1" --build-arg QUANTUM_DB_USER="api" --build-arg QUANTUM_DB_PASS="WofeZohiFuji" --build-arg QUANTUM_DB_HOST="localhost" .

push-image:
	docker tag bqp-api:${VERSION} ${DOCKERHUB}/bqp-api:${VERSION}
	docker tag ${DOCKERHUB}/bqp-api:${VERSION} ${DOCKERHUB}/bqp-api
	docker push ${DOCKERHUB}/bqp-api:${VERSION}
	docker push ${DOCKERHUB}/bqp-api
