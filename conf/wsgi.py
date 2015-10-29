"""
WSGI config for OSQA project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""

import os
import sys
current_dir = os.path.dirname(os.path.realpath(__file__))
osqa_dir = current_dir[:current_dir.rfind('/')]
parent_dir = current_dir[:osqa_dir.rfind('/')]

sys.path.append(parent_dir)
sys.path.append(osqa_dir)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "osqa.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
