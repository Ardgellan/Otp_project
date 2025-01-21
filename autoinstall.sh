#!/bin/bash

Red=$'\e[1;31m'
Green=$'\e[1;32m'
Blue=$'\e[1;34m'
Defaul_color=$'\e[0m'
Orange=$'\e[1;33m'
White=$'\e[1;37m'

#ask for bot token
echo "Enter bot token:"
echo "You can get it from $Blue @BotFather"
read bot_token

#ask user for Database user
echo ""
echo "Enter TOTP secret:"
echo "Just press ENTER for use default TOTP secret [$Blue 123456 $White]" | sed 's/\$//g'
read totp_secret
if [ -z "$totp_secret" ]
then
      totp_secret="123456"
fi

echo ""
echo "Enter admins ids (separated by comma):"
echo "Just press ENTER for use default ids [$Blue 123456789, $White]" | sed 's/\$//g'
echo "You can get your id by sending /id command to @userinfobot"
read admins_ids
if [ -z "$admins_ids" ]
then
      admins_ids="123456789,"
fi

echo ""
echo "Enter Database name:"
echo "Just press ENTER for use default name [$Blue vpnizator_database $White]" | sed 's/\$//g'
read database_name
if [ -z "$database_name" ]
then
      database_name="vpnizator_database"
fi

#ask user for Database user
echo ""
echo "Enter Database user:"
echo "Just press ENTER for use default user [$Blue vpnizator_database_user $White]" | sed 's/\$//g'
read database_user
if [ -z "$database_user" ]
then
      database_user="vpnizator_database_user"
fi

#ask user for Database password
echo ""
echo "Enter Database user password:"
echo "Just press ENTER for use default password [$Blue starscream $White]" | sed 's/\$//g'
read database_passwd
if [ -z "$database_passwd" ]
then
      database_passwd="starscream"
fi

#all neccessary data is collected
echo ""
echo "All neccessary data is collected"
echo "Now script will install all needed software (it can take some time)"
echo "$White" | sed 's/\$//g'
echo "Wanna update system before install? [y/N]"
echo "$Defaul_color" | sed 's/\$//g'
read update_system
if [ "$update_system" = "y" ]
then
      sudo apt update && sudo apt upgrade -y
fi

#some builds minimize system, unminimize it to get all default utilities
yes | unminimize

sudo apt install -y curl
#clear screen after install curl
clear

#install packages
sudo apt install -y git bat tmux mosh postgresql postgresql-contrib
systemctl start postgresql.service

#install python3.11 and pip
sudo apt install -y software-properties-common
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt install -y python3.11 python3.11-dev python3.11-distutils python3.11-venv
sudo curl https://bootstrap.pypa.io/get-pip.py -o /root/get-pip.py
python3.11 /root/get-pip.py

#install poetry
pip3.11 install poetry

#configure postgresql
su - postgres -c "psql -c \"CREATE USER $database_user WITH PASSWORD '$database_passwd';\""
su - postgres -c "psql -c \"CREATE DATABASE $database_name;\""
su - postgres -c "psql -c \"GRANT ALL PRIVILEGES ON SCHEMA public TO $database_user;\""
su - postgres -c "psql -c \"GRANT ALL PRIVILEGES ON DATABASE $database_name TO $database_user;\""

sudo timedatectl set-timezone Europe/Moscow

#clone bot repo
cd ~
git clone https://github.com/Ardgellan/Otp_project.git

#create venv and install bot dependencies
cd ~/Otp_project
poetry install --no-root
cd

sudo cat <<EOF > ~/Otp_project/source/data/.env
TG_BOT_TOKEN = "$bot_token"
TOTP_SECRET = "$totp_secret"
ADMINS_IDS = "$admins_ids"

DB_NAME = "$database_name"
DB_USER = "$database_user"
DB_USER_PASSWORD = "$database_passwd"
DB_HOST = "localhost"
DB_PORT = "5432"
EOF

#create and configure database
cd ~/Otp_project
$(poetry env info --path)/bin/python3.11 create_database_tables.py || sudo -u postgres psql -c "ALTER USER $database_user WITH SUPERUSER;" && $(poetry env info --path)/bin/python3.11 create_database_tables.py
cd

sudo cat <<EOF > /etc/systemd/system/otp_project.service
[Unit]
Description=OTP Authomation
After=network.target

[Service]
Type=simple
User=$current_os_user
ExecStart=/bin/bash -c 'cd ~/Otp_project/ && $(poetry env info --executable) main.py'
Restart=on-failure

[Install]
WantedBy=multi-user.target
EOF
cd

#enable and start bot service
systemctl daemon-reload
systemctl enable otp_project.service
systemctl start otp_project.service

