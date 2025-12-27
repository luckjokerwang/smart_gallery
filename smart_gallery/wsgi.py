"""
WSGI config for smart_gallery project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os
import sys  # <--- 新加这行

# 👇👇👇 新加这两行 (把 Conda 的库路径硬塞给 Python)
# 这一步是告诉 Python："不管你是谁启动的，一定要去这里找 Django！"
sys.path.append('/home/wzy/miniconda3/envs/others/lib/python3.12/site-packages')
# 👆👆👆

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smart_gallery.settings')

application = get_wsgi_application()
