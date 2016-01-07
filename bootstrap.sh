#!/bin/bash

# NB Run the script with root privileges
echo "Bootstrapping…"
# Comment out the CD-ROM from /etc/apt/sources.list:
sed  -i 's/^deb cdrom/# deb cdrom/' /etc/apt/sources.list

echo "Trying to update."
# Try updating the system a few times
apt-get update

loop = 1
while [ $? != 0 && $loop -le 3 ]
do
   apt-get update
   ((loop++))
done

echo "Trying to install packages."
# Install development environment dependencies:
apt-get --yes --force-yes install uzbl matchbox-window-manager xinit git pgadmin3 \
postgresql postgresql-client-9.4 postgresql-contrib-9.4 postgresql-server-dev-9.4 \
python-dev python-pip python-psycopg2 libffi-dev libpq-dev

pip install sh
#pip install Django
#pip install Django --upgrade # just to make sure
# pip install virtualenv
pip install -r /vagrant/requirements.txt

# Set up postgres
sudo -u postgres createdb hisra_db
sudo -u postgres psql -c "CREATE USER django_user WITH PASSWORD 'k3k3KUUSI'; \
ALTER ROLE django_user SET client_encoding TO 'utf8'; \
ALTER ROLE django_user SET default_transaction_isolation TO 'read committed'; \
ALTER ROLE django_user SET TIMEZONE to 'UTC'; \
GRANT ALL PRIVILEGES ON DATABASE hisra_db TO django_user;"

if [ $? != 0 ]
then
   echo "Something went wrong. You may try to install the packages manually or run the script again."
else
   echo "Bootstrap complete. Enjoy your development environment!"
fi
