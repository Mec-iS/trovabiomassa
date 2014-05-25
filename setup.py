from setuptools import setup

setup(name='Trovabiomassa-EU',
      version='1.0',
      description='Biomasses Finder Multilanguages',
      author='Lorenzo @lorenzogotuned',
      author_email='tunedconsulting@gmail.com',
      url='http://www.trovabiomassa.com',
      install_requires=['Django==1.6.2','django-redis', 'Pillow>=2.0', 'django-cms==3.0', 'django-classy-tags>=0.5',
                      'South==0.8.4', 'html5lib==1.0b1', 'django-mptt==0.6', 'django-sekizai==0.7',
                      'six==1.3.0', 'djangocms-admin-style==0.1.2', 'djangocms-text-ckeditor==2.1.4', 'djangocms-link' ],
     )
