.PHONY: install
install:
	pip install -r requirements.txt

.PHONY: create-db
create-db: install
	. ./.env && \
		flask cli create-db

.PHONY: init-db
init-db: install
	rm -rf migrations
	. ./.env && \
		flask db init

.PHONY: migrate
migrate: install
	. ./.env && \
		flask db migrate && flask db upgrade

.PHONY: drop-db
drop-db: install
	. ./.env && \
		flask cli drop-db

.PHONY: run
run: install
	. ./.env && \
		flask run
