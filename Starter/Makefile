#compose_file = docker-compose.yml
compose_file = docker-compose-dev.yml

run:
	docker compose -f $(compose_file) up
site-open:
	xdg-open http://127.0.0.1:8010/
admin-open:
	xdg-open http://127.0.0.1:8010/admin/
make-migrations:
	docker compose -f $(compose_file) run --rm web python manage.py makemigrations
collect-static:
	docker compose -f $(compose_file) run --rm web python manage.py collectstatic

migrate:
	docker compose -f $(compose_file) run --rm web python manage.py migrate

create-superuser:
	docker compose -f $(compose_file) run --rm web python manage.py createsuperuser

clear-sessions:
	docker compose -f $(compose_file) run --rm web python manage.py clearsessions
	
shell:
	docker compose -f $(compose_file) run --rm web python manage.py shell

load-sisa-info:
	docker compose -f $(compose_file) run --rm web python manage.py sisa

load-initial-data:
	docker compose -f $(compose_file) run --rm web python manage.py loaddata \
	insurance_company.Commission.json \
	agro.ClientLandConfiguration.json \
	capital.Taxes.json \
	agro.CropType.json \
	agro.Crop.json \
	agro.RateType.json \
	agro.Variable.json \
	agro.Campaign.json \
	insurance_company.Company.json \
	insurance_company.CompanyHierarchy.json \
	insurance_company.TypeFranchise.json \
	insurance_company.Franchise.json \
	fixtures/capital.paymentmethod.json \
	fixtures/capital.currency.json \
	afip.PersonType.json \
	afip.TaxCondition.json \
	insurance_company.ReSeeding.json \
	fixtures/agro.cropcompany.json \
	capital.Taxes.json

create-commission:
	docker compose -f $(compose_file) run --rm web python manage.py create_company_commission

load-geo:
	docker compose -f $(compose_file) run --rm web python manage.py get_provincias
	docker compose -f $(compose_file) run --rm web python manage.py get_departamentos
	docker compose -f $(compose_file) run --rm web python manage.py get_localidades

update-afip-codes:
	docker compose -f $(compose_file) run --rm web python manage.py update_province_afip

old-db-inspect:
	docker compose -f $(compose_file) run --rm web python manage.py inspectdb learni_visred --database=old

old-db-to-django-model:
	docker compose -f $(compose_file) run --rm web python manage.py inspectdb --database=old > old_models.py

migrate-old-data:
	docker compose -f $(compose_file) run --rm web python manage.py migrate --database=old

destroy-everything:
	docker compose -f $(compose_file) down --rmi all --volumes

purge-docker-db:
	sudo rm -rf ./data/ -R

resetmigrations:
	find . -path "*/migrations/*.py" -not -name "__init__.py" | grep -v "^./venv" | xargs rm
	find . -path "*/migrations/*.pyc"  -delete

resetmigrations-in-windows:
	powershell.exe -ExecutionPolicy Bypass -File resetmigrations.ps1

reset-database:
	python manage.py delete_transactions
	python manage.py delete_categories

load-geo-from-cache:
	docker compose -f $(compose_file) run --rm web python manage.py loaddata geo_backup.json

rebuild:
	docker compose -f $(compose_file) down --rmi all --volumes
	make purge-docker-db
	make resetmigrations
	docker compose -f $(compose_file) up

company-load-icon:
	docker compose -f $(compose_file) run --rm web python manage.py company_load_icon
company-create-additional:
	docker compose -f $(compose_file) run --rm web python manage.py company_add_additionals

rebuild-data:
	make make-migrations
	make migrate
	make create-superuser
#	make migrate-old-data
	make load-initial-data
	make create-commission
	make company-load-icon
	make company-create-additional
	make load-sisa-info
#	make load-geo
	make load-geo-from-cache
	make update-afip-codes

dam-migrate:
	docker compose -f $(compose_file) run --rm web python manage.py migrate --database=workshop_db
