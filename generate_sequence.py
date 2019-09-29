import numpy as np
from image_utils import get_digits, combine_images

import argparse

def generate_numbers_sequence(digits, spacing_range, image_width
                              , dataset_regime='train', image_save_name='combined_sequence.png'
                              , *args, **kwargs):
	"""
	:param digits: sequence of digits as a comma separated numbers 0-9
	:param spacing_range: the range of allowable spacing between digits chosen by uniform random distribution
	:param image_width: width of the combined image
	:param dataset_regime: regime of MNIST data
	:param image_save_name: save name for combined image
	:return: float32 array of combined digit image
	"""
	from PIL import Image
	from mnist_loader import MNISTLoader

	mnist_ds = MNISTLoader(dataset_regime)

	img_extents, img_array = get_digits(digits, mnist_ds)
	img_sequence = combine_images(img_array, img_extents, spacing_range, image_width)
	img_sequence = img_sequence.astype(np.uint8)

	Image.fromarray(img_sequence).save(image_save_name)

	return (img_sequence/255.).astype(np.float32)


def main():
	parser = argparse.ArgumentParser(
		description="Simple feature extraction"
	)
	parser.add_argument('-d', '--digits', type=int, nargs="+", help='sequence of numbers to generate')
	parser.add_argument('-s', '--spacing_range', nargs=2, type=int, help='min/max range of spacing between digits')
	parser.add_argument('-w', '--image_width', type=int, help='width of final image of sequence of digits')
	parser.add_argument('--dataset_regime', type=str, default='train'
	                    , help='MNIST dataset regime: "train" or "test"')
	parser.add_argument('--image_save_name', type=str, default='combined_sequence.png'
	                    , help='image file name for combined image')

	args = parser.parse_args()
	generate_numbers_sequence(**vars(args))

if __name__=="__main__":
	main()