import os

os.system('python manage.py backup_icpc_tolocal && python manage.py restore_icpc')
os.system('python manage.py backup_design_tolocal && python manage.py restore_design')