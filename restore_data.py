import os
os.system('python manage.py migrate')
os.system('python manage.py loaddata initial_data.json')
os.system('python manage.py restore_icpc')
os.system('python manage.py restore_design')
os.system('python manage.py createsuperuser')