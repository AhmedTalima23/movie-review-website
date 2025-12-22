#!/usr/bin/env python
import os
import sys
import django

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MovieReveiw.settings')

# Setup Django
django.setup()

from Page1.models import User, Movie, Review, Admin

def check_models():
    print("Checking model fields...")

    print("\nUser model fields:")
    for field in User._meta.fields:
        print(f"  - {field.name}: {field.__class__.__name__}")

    print("\nMovie model fields:")
    for field in Movie._meta.fields:
        print(f"  - {field.name}: {field.__class__.__name__}")

    print("\nReview model fields:")
    for field in Review._meta.fields:
        print(f"  - {field.name}: {field.__class__.__name__}")

    print("\nAdmin model fields:")
    for field in Admin._meta.fields:
        print(f"  - {field.name}: {field.__class__.__name__}")

if __name__ == '__main__':
    check_models()