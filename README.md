# schoolar_web_scraping

yedekleme
docker exec -t postgres pg_dump -U admin -d cities > cities_backup.sql


yedeği geri yükleme
cat cities_backup.sql | docker exec -i postgres psql -U admin -d cities
