import os
import gzip
import struct
import random
import numpy as np
from MNIST_number_sequence import config

import tqdm

IMG_HEIGHT = 28
IMG_WIDTH = 28
IMG_SIZE = IMG_HEIGHT * IMG_WIDTH

class MNISTLoader:
	"""
	train image: http://yann.lecun.com/exdb/mnist/train-images-idx3-ubyte.gz
	train labels: http://yann.lecun.com/exdb/mnist/train-labels-idx1-ubyte.gz
	test image: http://yann.lecun.com/exdb/mnist/t10k-images-idx3-ubyte.gz
	test labels: http://yann.lecun.com/exdb/mnist/t10k-labels-idx1-ubyte.gz
	"""

	DATASET_LOCATIONS = {"train": {"images": ["datasets/train-images-idx3-ubyte.gz"
		, "http://yann.lecun.com/exdb/mnist/train-images-idx3-ubyte.gz"]
		, "labels": ["datasets/train-labels-idx1-ubyte.gz"
			, "http://yann.lecun.com/exdb/mnist/train-labels-idx1-ubyte.gz"]}
		, "test": {"images": ["datasets/t10k-images-idx3-ubyte.gz"
			, "http://yann.lecun.com/exdb/mnist/t10k-images-idx3-ubyte.gz"]
			, "labels": ["datasets/t10k-labels-idx1-ubyte.gz"
				, "http://yann.lecun.com/exdb/mnist/t10k-labels-idx1-ubyte.gz"]}}

	MAGIC_NUMS = [2051, 2049]  # image, label magic numbers
	DATASET_COUNTS = {"train": 60000, "test": 10000}  # train, test

	IMG_OFFSET = 16
	LABEL_OFFSET = 8

	def __init__(self, dataset_regime="train"):
		# check if dataset files already exist:
		# image/label files
		local_datasets = [self.DATASET_LOCATIONS[dataset_regime][key][0] for key in self.DATASET_LOCATIONS[dataset_regime].keys()]
		url_datasets = [self.DATASET_LOCATIONS[dataset_regime][key][1] for key in self.DATASET_LOCATIONS[dataset_regime].keys()]
		for idx, dataset in enumerate(local_datasets):
			f_path = os.path.join(config.ROOT_DIR, dataset)
			set = list(self.DATASET_LOCATIONS[dataset_regime].keys())[idx]
			if not os.path.isfile(f_path):
				import urllib.request
				url = url_datasets[idx]
				try:
					resp = urllib.request.urlopen(url)
					length = int(resp.headers['Content-Length'])
				except:
					raise Exception(f'Could not open {url}')

				with open(f_path, 'wb+') as fh:
					for i in tqdm.tqdm(range(1024, length, 1024)
							, desc=f'Downloading MNIST dataset {dataset_regime} {set}', position=0):
						try:
							buff = resp.read(i)
							fh.write(buff)
						except:
							raise Exception(f'Could not write buffer to file {f_path}')

		self._check_integrity(local_datasets, dataset_regime)
		self._load_images(local_datasets[0], dataset_regime)
		self._create_digit_hash(local_datasets[1], dataset_regime)

	def _check_integrity(self, dataset_paths, dataset_regime):
		dataset_cnts = self.DATASET_COUNTS[dataset_regime]
		for idx, datasets in enumerate(dataset_paths):
			f_path = os.path.join(config.ROOT_DIR, datasets)
			with gzip.open(f_path, 'rb') as f:
				magic_num, counts = struct.unpack(">II", f.read(8))
			if magic_num != self.MAGIC_NUMS[idx]:
				raise Exception(f"Corrupted datasets: magic numbers do not match: {magic_num} != {self.MAGIC_NUMS[idx]}")
			if counts != dataset_cnts:
				raise Exception(f"Corrupted datasets: dataset counts do not match: {counts} != {dataset_cnts}")

	def _load_images(self, dataset_image_path, dataset_regime):
		f_path = os.path.join(config.ROOT_DIR, dataset_image_path)
		with gzip.open(f_path, 'rb') as f:
			f.seek(self.IMG_OFFSET)
			self.digit_images = np.fromstring(f.read(), dtype='>B')

			self.digit_images = self.digit_images.reshape((self.DATASET_COUNTS[dataset_regime], IMG_HEIGHT, IMG_WIDTH))

	def _create_digit_hash(self, dataset_paths, dataset_regime):
		digit_hash = {i: [] for i in range(10)}
		f_path = os.path.join(config.ROOT_DIR, dataset_paths)
		with gzip.open(f_path, 'rb') as f:
			f.seek(self.LABEL_OFFSET)
			line = f.read(1)
			line_idx = 0
			while line:
				digit_label = struct.unpack(">B", line)[0]
				digit_hash[digit_label] += [line_idx]
				line_idx += 1
				line = f.read(1)
		assert sum([len(digit_hash[key]) for key in digit_hash.keys()]) == self.DATASET_COUNTS[dataset_regime]
		self.digit_hash = digit_hash

	def get_image_at(self, idx):
		return self.digit_images[idx]

	def get_digit_image(self, digit):
		return self.get_image_at(random.choice(self.digit_hash[digit]))




"""
DATASET_LOCATIONS = {"train": {"images" : ["datasets/train-images-idx3-ubyte.gz"
											, "http://yann.lecun.com/exdb/mnist/train-images-idx3-ubyte.gz"]
								, "labels": ["datasets/train-labels-idx1-ubyte.gz"
											, "http://yann.lecun.com/exdb/mnist/train-labels-idx1-ubyte.gz"]}
						,"test": {"images": ["datasets/t10k-images-idx3-ubyte.gz"
						                     , "http://yann.lecun.com/exdb/mnist/t10k-images-idx3-ubyte.gz"]
								, "labels": ["datasets/t10k-labels-idx1-ubyte.gz"
											, "http://yann.lecun.com/exdb/mnist/t10k-labels-idx1-ubyte.gz"]}}

MAGIC_NUMS = [2051, 2049] # image, label magic numbers
DATASET_COUNTS = {"train": 60000, "test": 10000} # train, test

IMG_OFFSET=16
IMG_HEIGHT=28
IMG_WIDTH=28
IMG_SIZE= IMG_HEIGHT * IMG_WIDTH
LABEL_OFFSET=8
DIGIT_HASH=None

def load_dload_dataset(segment="train"):
	# check if dataset files already exist:
	# image/label files
	local_datasets = [DATASET_LOCATIONS[segment][key][0] for key in DATASET_LOCATIONS[segment].keys()]
	url_datasets = [DATASET_LOCATIONS[segment][key][1] for key in DATASET_LOCATIONS[segment].keys()]
	for idx, dataset in enumerate(local_datasets):
		if not os.path.isfile(dataset):
			import urllib.request
			url = url_datasets[idx]
			urllib.request.urlretrieve(url, dataset)

	_check_integrity(local_datasets, segment)

	global DIGIT_HASH
	DIGIT_HASH = _create_digit_hash(local_datasets[1], segment)


def _check_integrity(dataset_paths, segment):
	dataset_cnts = DATASET_COUNTS[segment]
	for idx, datasets in enumerate(dataset_paths):
		with gzip.open( datasets, 'rb') as f:
			magic_num, counts = struct.unpack(">II", f.read(8))
		if magic_num != MAGIC_NUMS[idx]:
			raise Exception(f"Corrupted datasets: magic numbers do not match: {magic_num} != {MAGIC_NUMS[idx]}")
		if counts != dataset_cnts:
			raise Exception(f"Corrupted datasets: dataset counts do not match: {counts} != {dataset_cnts}")

def _create_digit_hash(dataset_paths, segment):
	digit_hash = {i:[] for i in range(10)}
	with gzip.open(dataset_paths, 'rb') as f:
		f.seek(LABEL_OFFSET)
		line = f.read(1)
		line_idx = 0
		while line:
			digit_label = struct.unpack(">B", line)[0]
			digit_hash[digit_label] += [line_idx]
			line_idx += 1
			line = f.read(1)
	assert sum([len(digit_hash[key]) for key in digit_hash.keys()]) == DATASET_COUNTS[segment]
	return digit_hash

def get_img_label(data_idx):
	img = _get_image_at(data_idx)
	label = _get_label_at(data_idx)
	return label, img


def _get_image_at(data_idx):
	with gzip.open('datasets/train-images-idx3-ubyte.gz', 'rb') as f:
		f.seek(IMG_SIZE*data_idx + IMG_OFFSET)
		im_buffer = f.read(IMG_SIZE)
		im_buffer = np.frombuffer(im_buffer, dtype=np.dtype('>B') ).reshape((IMG_WIDTH, IMG_HEIGHT)) # 0-255 image
		return im_buffer.copy()


def _get_label_at(data_idx):
	with gzip.open('datasets/train-labels-idx1-ubyte.gz', 'rb') as f:
		f.seek(data_idx + LABEL_OFFSET)
		return struct.unpack(">B", f.read(1))[0]
"""




