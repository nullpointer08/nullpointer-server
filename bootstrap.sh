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
apt-get --yes --force-yes install uzbl
apt-get --yes --force-yes install matchbox-window-manager
apt-get --yes --force-yes install xinit
apt-get --yes --force-yes install git
apt-get --yes --force-yes install pgadmin3
apt-get --yes --force-yes install postgresql
apt-get --yes --force-yes install postgresql-client-9.4
apt-get --yes --force-yes install postgresql-contrib-9.4
apt-get --yes --force-yes install postgresql-server-dev-9.4
apt-get --yes --force-yes install python-dev
apt-get --yes --force-yes install python-pip
apt-get --yes --force-yes install python-psycopg2
pip install sh
pip install Django
pip install Django --upgrade # just to make sure
pip install virtualenv

if [ $? != 0 ]
then
   echo "Something went wrong. You may try to install the packages manually or run the script again."
else
   echo "Bootstrap complete. Enjoy your development environment!"
fi
