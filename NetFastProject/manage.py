#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    """Run administrative tasks."""
    # Pastikan Django memuat settings sebagai paket project
    # Gunakan 'NetFastProject.settings' sehingga modul dapat diimport
    # ketika menjalankan `python NetFastProject\manage.py ...` dari root repo
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NetFastProject.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()