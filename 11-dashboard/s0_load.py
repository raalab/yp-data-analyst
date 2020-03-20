# -*- coding: utf-8 -*-

sudo su postgresudo apt update
sudo apt install python3-pip
sudo apt install postgresql postgresql-contrib
sudo apt-get install python3-psycopg2 

pip3 install sqlalchemy 
pip3 install pandas
pip3 install dash 

echo ... СТАРТ Postgresql ...
sudo service postgresql start
echo ... СТАТУС Postgresql ...
service postgresql status

# sudo su postgres
# createdb zen
# psql -d zen
# 	CREATE USER my_user WITH ENCRYPTED PASSWORD 'my_user_password';
# 	GRANT ALL PRIVILEGES ON DATABASE zen TO my_user;
# pg_restore -d zen /tmp/zen_raw.dump
# pg_dump -Fc zen> /tmp/zen.dump
# sudo cp /tmp/games.dump /ПУТЬ_К_ПАПКЕ_ДЛЯ_ХРАНЕНИЯ_ДАМПА