sudo apt install python3-python manage.pypip
pip3 install virtualenv
python3.7 -m venv venv
source venv/bin/activate

pip install -r requirements.txt

python manage.py runserver

