import os
import django
from django.contrib.auth import get_user_model

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings') # Replace 'project.settings' with your actual settings module
django.setup()

User = get_user_model()

email = 'admin@code.com'
password = 'Test@1234'

if not User.objects.filter(email=email).exists():
    print(f'Creating superuser with email {email}')
    User.objects.create_superuser(email=email, password=password)
else:
    print(f'Superuser with email {email} already exists.') 