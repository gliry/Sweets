1) Open a console, connect to the server via ssh:
ssh entrant@178.154.209.188
Enter the password, check the location on the server with the pwd or ls -la commands.

2) Save project libraries:
pip freeze> requirements.txt
Save the project in .zip format. If there is a repository on github, skip this and the next paragraph.

3) Open PowerShell and write the command:
scp <path> entrant @ entrant @ 178.154.209.188: / home / entrant
Enter your password.

4) Next, enter the following commands in the console:

sudo apt update
If Zip file:
sudo apt install unzip
unzip <name of .zip file>
if git then skip the 2 commands above

sudo apt install python3-pip
sudo apt install python3-dev
sudo apt install postgresql
sudo apt install libpq-dev
sudo apt install net-tools
sudo apt install git
sudo apt install gunicorn
pip3 install psycopg2
pip3 install -r requirements.txt
pip3 install gunicorn
pip3 install psycopg2-binary

5) Let's configure the database:
sudo so - postgres
psql
CREATE DATABASE couriers;
\ password
postgresql

6) If the project was in the repository on github, then:
git clone <link to repository>
If necessary, enter your github username and password.

7) Let's migrate:
python3 manage.py makemigrations
python3 manage.py migrate

8) Start the server
python3 manage.py runserver 0.0.0.0:8080
Or:
gunicorn --bind 0.0.0.0:8080 sweet.wsgi
(the latter is preferred)
	
