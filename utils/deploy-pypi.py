import os, shutil
import xmlrpc.client
from subprocess import Popen, PIPE
from setuptools import find_packages
from natsort import natsorted

###### CONFIGURATIONS #############################
HEADER    = '\033[95m'
OKBLUE    = '\033[94m'
OKGREEN   = '\033[92m'
WARNING   = '\033[93m'
FAIL 	  = '\033[91m'
ENDC 	  = '\033[0m'
BOLD 	  = '\033[1m'
UNDERLINE = '\033[4m'

DEBUG  = False
DEPLOY = True

if DEBUG:
	PYPI_URL = 'https://test.pypi.org'
else:
	PYPI_URL = 'https://pypi.org'

# Dictionary with the correspondence of the libraries and folders.
PACKAGES = { 'pyforms-web': 'pyforms_web' }
PACKAGES_TO_IGNORE = []

# sub packages directories to look for updates
DIRECTORIES_TO_SEARCH_FORM = [
	os.path.join('libraries'),
	os.path.join('plugins'),
]

APP_DIRECTORY = os.getcwd() # current directory

####################################################

pypi = xmlrpc.client.ServerProxy(PYPI_URL)

# make sure all the packages required to deploy to pypi are installed
Popen(['pip','install','--upgrade','setuptools','wheel','twine']).communicate()


def version_compare(a, b):
	"""
	Compare versions
	:param a: Version a
	:param b: Version b
	:return: Returns 0 if equal, returns 1 if a>b, returns -1 if b>a
	"""
	if a == b: return 0
	versions = natsorted([a, b])
	if a==versions[-1]: return -1
	if b==versions[-1]: return 1
	raise Exception('Error when comparing versions')



def update_package_version(package_name, setup_path, new_version):
	"""
	Update the version of the package

	:param str package_name: Package name.
	:param str setup_path: Path of the setup.py file.
	:param str new_version: The new version to update.
	:return:
	"""
	if package_name in PACKAGES:
		package = PACKAGES[package_name]
	else:
		packages = find_packages(where=setup_path)
		package  = packages[0]

	package_path = os.path.join(setup_path, package)
	init_path = os.path.join(package_path, '__init__.py')

	with open(init_path) as infile: text = infile.read()
	try:
		begin = text.index('__version__')
		end   = text.index('\n', begin)
		text  = text.replace( text[begin:end], f'__version__ = "{new_version}"')
	except ValueError:
		text = text + f'\n__version__ = "{new_version}"'

	with open(init_path, 'w') as outfile: outfile.write(text)



def check_version_and_upload(dir_path):
	"""
	Check the package version and decide if should be updated or not.
	:param str dir_path: Path of the package.
	"""
	os.chdir(dir_path)

	try:
		shutil.rmtree(os.path.join(dir_path, 'build'))
	except OSError:
		pass
	except Exception as e:
		print(e)
	try:
		shutil.rmtree(os.path.join(dir_path, 'dist'))
	except OSError:
		pass
	except Exception as e:
		print(e)

	local_version = Popen(["python", 'setup.py', '--version'], stdout=PIPE).stdout.read()
	local_version = local_version.strip().decode().strip()

	package_name = Popen(["python", 'setup.py', '--name'], stdout=PIPE).stdout.read()
	package_name = package_name.strip().decode().replace(' ', '-')
	package_name = package_name.replace('---', '-').lower()

	if package_name in PACKAGES_TO_IGNORE:
		os.chdir(APP_DIRECTORY)
		return False, package_name, local_version

	tmp = pypi.package_releases(package_name)
	remote_version = tmp[0] if tmp else 'None'

	tagged_version = Popen(["git", "describe", "--tags"], stdout=PIPE).stdout.read()
	tagged_version = tagged_version.strip().decode().split('-')
	tagged_version = tagged_version[0]

	print(f"{OKGREEN}{package_name:<65} {local_version:<25} {tagged_version:<25} {remote_version:<25}{ENDC}")

	updated = False

	if remote_version=='None' or version_compare(tagged_version, remote_version) < 0:
		print(OKBLUE+f'\tUPLOADING TO PYPI\t\t[{package_name}]', ENDC)

		update_package_version(package_name, dir_path, tagged_version)

		if os.path.isdir('./dist'): shutil.rmtree('./dist')

		Popen(['python', 'setup.py', 'sdist', 'bdist_wheel'], stdout=PIPE).communicate()

		######################################################################################
		# DEPLOY TO PYPI #####################################################################
		######################################################################################
		if DEPLOY:
			if not DEBUG:
				Popen(['twine', 'upload', os.path.join('dist','*')]).communicate()
			else:
				Popen(['twine', 'upload', '--repository', 'pypitest', os.path.join('dist', '*'), '--verbose']).communicate()
		######################################################################################

		updated = True

	os.chdir(APP_DIRECTORY)

	return updated, package_name, tagged_version


# List of requirements
requirements = []

for search_dir in DIRECTORIES_TO_SEARCH_FORM:
	print(
		BOLD+HEADER+"\n{:<65} {:<25} {:<25} {:<25}".format('PACKAGE', 'LOCAL', 'TAGGED VERSION', 'REMOTE')+ENDC
	)

	for dir_name in os.listdir(search_dir):

		dir_path = os.path.abspath(os.path.join(search_dir, dir_name))

		setup_filepath = os.path.join(dir_path, 'setup.py')
		if not os.path.isfile(setup_filepath): continue

		updated, package_name, version = check_version_and_upload(dir_path)

		requirements.append("{module}=={version}".format(module=package_name, version=version))
