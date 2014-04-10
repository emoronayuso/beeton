import os
import site
#from setuptools import setup
try:
	from setuptools import setup
except ImportError:
	from distutils.core import setup
	import warnings
	#warnings('Por favor instala setuptools o distribute!')

#from pip.req import parse_requirements


README = open(os.path.join(os.path.dirname(__file__), 'README.md')).read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

# parse_requirements() returns generator of pip.req.InstallRequirement objects
#nstall_reqs = parse_requirements('requirements.txt')

# reqs is a list of requirement
# e.g. ['django==1.5.1', 'mezzanine==1.4.6']
#reqs = [str(ir.req) for ir in install_reqs]

#with open('requirements.txt') as f:
#	required = f.read().splitlines()


##Utilizar python setup.py install --user, se instalara en la ruta especificada
site.USER_SITE = '/var/www'

setup(
    name = 'django-beeton',
    version = '0.1',
    packages = ['asterisk-bee.asteriskbee'],
    include_package_data = True,
    license = 'GNU General Public License version 3(GPLv3)',
    description = 'Panel de administracion web de una PBX implementada con Asterisk',
    long_description = README,
    url = 'http://beeton.wordpress.com/',
    author = 'Enrique Moron Ayuso',
    author_email = 'emoronayuso@gmail.com',
    classifiers = [
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GPLv3 License',
        'Operating System :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        ],
    # install_requires = [ required , 'numpy==1.8.0' ,'datetime' ],

   )
