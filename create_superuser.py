# create_superuser.py

import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "infowebapp.settings")
django.setup()

from django.contrib.auth.models import User

username = "admin"
email = "mansi@gmail.com"
password = "4488man!#"

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password=password)
    print("Superuser created successfully.")
else:
    print("Superuser already exists.")
