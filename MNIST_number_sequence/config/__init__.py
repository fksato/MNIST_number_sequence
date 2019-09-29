import os
import sys

ROOT_DIR = os.path.dirname(os.path.abspath(sys.modules['__main__'].__file__))

if not os.path.isdir(os.path.join(ROOT_DIR, 'datasets')):
	os.mkdir(os.path.join(ROOT_DIR, 'datasets'))