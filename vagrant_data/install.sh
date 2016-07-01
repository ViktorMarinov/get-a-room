#!/bin/bash

USER_HOME=/home/vagrant

echo -e "\n\n"
echo "######################################"
echo "## Create dependencies download dir ##"
echo "## for the external services needed ##"
echo "######################################"

mkdir $USER_HOME/get_a_room/dependencies

echo -e "\n\n"
echo "####################"
echo "## Installing Git ##"
echo "####################"

apt-get install -y git-core

echo -e "\n\n"
echo "###########################"
echo "## Install PostgreSQL    ##"
echo "## Versiоn 9.4 (bit old) ##"
echo "###########################"

cd $USER_HOME/get_a_room/dependencies
# install dependencies for PostgreSQL to work with Django
apt-get install -y libpq-dev python-dev
# download ultra cool .sh script that will enable PostgreSQL APT
wget https://gist.githubusercontent.com/hhursev/4fbe4643e2304b0b315c/raw/574146ce201e18d1c9ecb0bf9932d4707410a104/postgresql.apt.sh
chmod +x postgresql.apt.sh
./postgresql.apt.sh

apt-get install -y postgresql-9.4
apt-get install -y postgresql-server-dev-9.4


# Remove password from default postgres user
sudo -u postgres psql template1 -x -c "ALTER ROLE postgres PASSWORD ''"


# Set configuration
cp $USER_HOME/get_a_room/vagrant_data/pg_hba.conf /etc/postgresql/9.4/main/pg_hba.conf
cp $USER_HOME/get_a_room/vagrant_data/postgresql.conf /etc/postgresql/9.4/main/postgresql.conf

# Restart postgres
service postgresql restart

# Create get_a_room database
sudo -u postgres psql -d postgres -c "CREATE DATABASE get_a_room;"

echo -e "\n\n"
echo "##########################"
echo "## Install Python 3.5.1 ##"
echo "##########################"

# to be able to compile Python from source, we will need few packages
apt-get install -y build-essential libncursesw5-dev libreadline6-dev
apt-get install -y libssl-dev libgdbm-dev libc6-dev libsqlite3-dev tk-dev

# download and build Python 3.5.1
cd $USER_HOME/get_a_room/dependencies
wget -O Python-3.5.1.tgz https://www.python.org/ftp/python/3.5.1/Python-3.5.1.tgz
tar xvzf Python-3.5.1.tgz
cd $USER_HOME/get_a_room/dependencies/Python-3.5.1
# Python 3.5.1 will be installed in /opt/python3
./configure --prefix=/opt/python3
make
make install


echo -e "\n\n"
echo "#################################"
echo "## Create project's virtualenv ##"
echo "#################################"

apt-get install -y python-pip
pip install virtualenv
pip install virtualenvwrapper

echo "source /usr/local/bin/virtualenvwrapper.sh" >> $USER_HOME/.bashrc
mkdir $USER_HOME/.virtualenvs
WORKON_HOME=$USER_HOME/.virtualenvs
source /usr/local/bin/virtualenvwrapper.sh

cd $USER_HOME/get_a_room
mkvirtualenv -a `pwd` -p /opt/python3/bin/python3.5 get_a_room
# Set vagrant as owner for virtualenvs
chown -R vagrant:vagrant $USER_HOME/.virtualenvs

workon get_a_room
pip install -r requirements/dev_requirements.txt

killall -9 python

echo -e "\n\n"
echo "#############################"
echo "## Successful installation ##"
echo "#############################"

echo -e "\nInstalled versions:"
(
git --version
$USER_HOME/.virtualenvs/local/bin/python3 --version
psql --version
virtualenv --version
) | sed -u "s/^/  /"

exit 0