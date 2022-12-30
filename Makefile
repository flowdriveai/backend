.PHONY: install
install:
	pip install -r requirements.txt

.PHONY: create-db
create-db: install
	source .env && \
		flask cli create-db

.PHONY: init-db
init-db: install
	rm -rf migrations
	source .env && \
		flask db init

.PHONY: migrate
migrate: install
	source .env && \
		flask db migrate && flask db upgrade

.PHONY: drop-db
drop-db: install
	source .env && \
		flask cli drop-db

.PHONY: run
run: install
	source .env && \
		flask run
