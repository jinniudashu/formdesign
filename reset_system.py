import os

os.system('python manage.py makemigrations && python manage.py migrate')
os.system('python manage.py loaddata initial_data.json')
os.system('python manage.py backup_icpc_tolocal && python manage.py restore_icpc')
os.system('python manage.py backup_design_tolocal && python manage.py restore_design')
os.system('phthon manage.py createsuperuser')