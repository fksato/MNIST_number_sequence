import numpy as np
from MNIST_number_sequence.image_utils import get_digits, combine_images
from MNIST_number_sequence.image_utils.image_transformations import skew

import argparse

def generate_skewed_numbers_sequence(digits, spacing_range, image_width
                                     , dataset_regime='train', image_save_name='combined_skewed_sequence.png'
                                     , skew_img=True, tight=True
                                     , *args, **kwargs):
	"""
	:param digits: sequence of digits as a comma separated numbers 0-9
	:param spacing_range: the range of allowable spacing between digits chosen by uniform random distribution
	:param image_width: width of the combined image
	:param dataset_regime: regime of MNIST data
	:param image_save_name: save name for combined image
	:param skew_img: skew a randomly selected number of digit images
	:return: float32 array of combined digit image
	"""
	from PIL import Image
	from MNIST_number_sequence.mnist_loader import MNISTLoader

	mnist_ds = MNISTLoader(dataset_regime)

	apply = None
	if skew_img:
		apply = skew

	img_extents, img_array = get_digits(digits, mnist_ds, tight=tight, apply=apply)
	img_sequence = combine_images(img_array, img_extents, spacing_range, image_width)
	img_sequence = img_sequence.astype(np.uint8)

	Image.fromarray(img_sequence).save(image_save_name)

	return (img_sequence/255.).astype(np.float32)


def main():
	parser = argparse.ArgumentParser(
		description="Simple feature extraction"
	)
	parser.add_argument('-d', '--digits', nargs="+", type=int, help='sequence of numbers to generate')
	parser.add_argument('-s', '--spacing_range', nargs=2, type=int, help='min/max range of spacing between digits')
	parser.add_argument('-w', '--image_width', type=int, default=None
	                    , help='width of final image of sequence of digits')
	parser.add_argument('--dataset_regime', type=str, default='train'
	                    , help='MNIST dataset regime: "train" or "test"')
	parser.add_argument('--image_save_name', type=str, default='combined_skewed_sequence.png'
	                    , help='image file name for combined image')
	parser.add_argument('--remove_skew', dest='skew_img', action='store_false'
	                    , help='Flag to ignore skewing of digit images')
	parser.add_argument('--make_tight', dest='tight', action='store_true'
	                    , help='Flag to calculate extents from most significant pixels')

	args = parser.parse_args()
	generate_skewed_numbers_sequence(**vars(args))

if __name__=="__main__":
	main()