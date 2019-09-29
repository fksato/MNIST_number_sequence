from setuptools import setup, find_packages

requirements = [
    "numpy",
    "Pillow",
	"tqdm",
    # test_requirements
    "pytest",
]

setup(
	name='MNIST_number_sequence',
	version='0.1.0',
	packages=find_packages(exclude=['tests']),
	url='https://github.com/fksato/MNIST_number_sequence',
	author='Fukushi Sato',
	author_email='f.kazuo.sato@gmail.com',
	description='generate a sequence of numbers from MNIST dataset',
	install_requires=requirements,
	classifiers=[
			        'Development Status :: Pre-Alpha',
			        'Intended Audience :: Developers',
			        'License :: MIT License',
			        'Natural Language :: English',
			        'Programming Language :: Python :: 3.6',
			        'Programming Language :: Python :: 3.7',
			    ],
	test_suite='tests',
)
