1) Открыть консоль, подключиться к серверу по ssh:
	ssh entrant@178.154.209.188
Ввести пароль, проверить командами pwd или ls -la нахождение на сервере.

2) Сохранить проект в формате .zip. Если есть репозиторий на github, пропустить этот и следующий пункты.

3) Открыть PowerShell и написать команду:
	scp <путь> entrant@entrant@178.154.209.188:/home/entrant
Ввести пароль. 

4) Далее в консоли ввести следующие команды:
	
	sudo apt update
	Если Zip file:
		sudo apt install unzip
		unzip <название .zip файла> 
	если git, то пропустить 2 команды выше

	sudo apt install python3-pip
	sudo apt install python3-dev
	sudo apt install postgresql
	sudo apt install libpq-dev
	sudo apt install net-tools
	sudo apt install git
	pip3 install psycopg2
	pip3 install -r requirements.txt

5)Настроим базу данных:
	sudo so - postgres
	psql
	CREATE DATABASE couriers;
	\password
	postgresql

6) Если проект был в репозитории на github, то:
	git clone <ссылка на репозиторий>
При необходимости ввести логин и пароль от github.

7)Сделаем migrate:
	python3 manage.py makemigrations
	python3 manage.py migrate

8) Запустить сервер 
	python3 manage.py runserver 0.0.0.0:8080
	
	
