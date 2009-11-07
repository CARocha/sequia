# -*- coding: utf-8 -*-

import os 

SITE_URL = 'localhost'
SITE_ROOT= os.path.dirname(__file__)
ADMINS = (('carlos', 'carlos@simas.org.ni'),)
EMAIL_HOST = 'localhost'
DEFAULT_FROM_EMAIL = 'carlos@simas.org.ni'
DATABASE_NAME = 'sequia.db'          
DATABASE_USER = ''           
DATABASE_PASSWORD = ''       
DATABASE_HOST = ''    #normalmente vacio cuando la base esta en la misma pc       
DATABASE_PORT = ''    #normalmente vacio cuando la base esta en la misma pc    
TIME_ZONE = 'America/Managua'
LANGUAGE_CODE = 'es-ni'
MEDIA_URL = 'http://localhost/'
SECRET_KEY = '7*^jamhqiba&11qbc6ld%7*j98(0)%egb(tb14i+r=0*6oozi='
