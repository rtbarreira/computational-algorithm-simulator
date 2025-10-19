IMAGE_NAME=clj-test-api
CONTAINER_NAME=clj-test-api-container
PORT=5000

.PHONY: build
build:
	docker build -t $(IMAGE_NAME) .

define run_in_container
	docker run --rm -p $(PORT):5000 --name $(CONTAINER_NAME) $(IMAGE_NAME) \
		sh -c "python3 api.py & sleep 5 && $(1)"
endef

.PHONY: coverage-all
coverage-all:
	$(call run_in_container, \
		curl -X POST http://localhost:$(PORT)/coverage; \
		curl -O http://localhost:$(PORT)/coverage/artifact; \
		unzip -o coverage-report.zip -d coverage-report; \
		echo 'Abrindo relatório Cloverage...'; \
		xdg-open coverage-report/index.html || open coverage-report/index.html)

.PHONY: mutation-all
mutation-all:
	$(call run_in_container, \
		curl -X POST http://localhost:$(PORT)/mutation; \
		curl -O http://localhost:$(PORT)/mutation/artifact; \
		unzip -o mutation-report.zip -d mutation-report; \
		echo 'Abrindo relatório Mutant...'; \
		xdg-open mutation-report/mutation-report.edn || open mutation-report/mutation-report.edn)

.PHONY: full
full:
	$(call run_in_container, \
		curl -X POST http://localhost:$(PORT)/coverage; \
		curl -O http://localhost:$(PORT)/coverage/artifact; \
		unzip -o coverage-report.zip -d coverage-report; \
		curl -X POST http://localhost:$(PORT)/mutation; \
		curl -O http://localhost:$(PORT)/mutation/artifact; \
		unzip -o mutation-report.zip -d mutation-report; \
		echo 'Abrindo relatório Cloverage...'; \
		xdg-open coverage-report/index.html || open coverage-report/index.html; \
		echo 'Relatório Mutant disponível em mutation-report/mutation-report.edn')
