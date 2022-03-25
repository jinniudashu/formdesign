import os

os.system('git pull origin main')
os.system('python manage.py backup_icpc_tolocal')
os.system('python manage.py backup_design_tolocal')
os.system('python manage.py migrate')
os.system('python manage.py loaddata initial_data.json')
os.system('python manage.py restore_icpc')
os.system('python manage.py restore_design')
os.system('phthon manage.py createsuperuser')