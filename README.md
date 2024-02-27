# schoolar_web_scraping

yedekleme
docker exec -t postgres pg_dump -U admin -d cities > all_data_backup2.sql


yedeği geri yükleme
cat cities_backup.sql | docker exec -i postgres psql -U admin -d cities
