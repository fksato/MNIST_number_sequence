from setuptools import setup

requirements = [
    "numpy",
    "Pillow",
	"tqdm",
    # test_requirements
    "pytest",
]

setup(
	name='number_sequence_generator',
	version='0.1.0',
	packages=['config', 'image_utils', 'mnist_loader'],
	url='',
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
