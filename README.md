1. Clone the project.
2. Create a virtual environment.
```
pip install virtualenv
virtualenv venv
venv\Scripts\activate
```
3. Install the requirements:
```
pip install -r requirements.txt
```
4. Loading fixtures:
```
python manage.py loaddata data.json
```
5. Run the command:
```
python manage.py runserver
```
-------------------------------------------------------------------------------------------------------------------------
7. If you want to change the portable/Docker mode, run the swap_env.py file and select the mode. The default is portable.
```
python swap_env.py
```
```
(input) portable/remote
```
8. If you are using remote(Docker) mode, run the command:
docker-compose up
