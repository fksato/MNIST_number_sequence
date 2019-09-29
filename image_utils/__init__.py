import warnings
import numpy as np
from mnist_loader import IMG_HEIGHT, IMG_WIDTH


def get_digits(digits, mnist_images_ds, tight=False, apply=None):
	"""
	:param digits: sequence of digits 0-9
	:param mnist_images_ds: MNIST dataset object
	:param tight: calculate digit image extents where pixels are non-zero
	:param apply: Image transformations to apply
	:return:
	"""
	if not isinstance(digits, list):
		digits = [digits]

	image_array = []
	image_widths = []
	for digit in digits:
		digit_img = mnist_images_ds.get_digit_image(digit)
		# apply transformations for a select number of digits:
		if apply is not None and digit % 2 == 0:
			digit_img = apply(digit_img)
		# compute extents
		digit_extent = calculate_img_extent(digit_img, tight)
		# store image
		image_array.append(digit_img)
		image_widths.append(digit_extent)

	return image_widths, image_array


def combine_images(image_array, image_extents, min_max_spacing, image_width=None):
	"""
	:param image_array: a list of images
	:param image_extents: a list of tuples of each image extents
	:param min_max_spacing: minimum/maximum spacing allowed between digits (in pixels)
	:param image_width: final width of combined images. If None, compute image width
	:return: a single image created by the combination of images in image array
	"""
	digit_image_widths = [extents[1] - extents[0] for extents in image_extents]
	num_images = len(image_array)
	image_starts = []

	if min(digit_image_widths) < abs(min_max_spacing[0]):
		warnings.warn('Provided spacing between digits can produce an image '
		              'in which digits are not strictly sequential')

	if image_width is None or image_width == 0:
		image_width = 0
		combined_image_width = 1
	else:
		if not check_valid_input_width(image_width, digit_image_widths, num_images, min_max_spacing):
			raise Exception(f'Image width {image_width} is too small to fit the sequence of digits')

		combined_image_width = image_width + 1

	# check if random spacing needs to be validated
	validate_starts = True

	while combined_image_width > image_width or validate_starts:
		# allowing for the possibility of overlapping digits, min_spacing can be < 0:
		image_starts = np.random.randint(min_max_spacing[0], min_max_spacing[1], num_images + 1)
		# check for starting/ending index is greater than equal to 0:
		image_starts[0] = max(0 + image_starts[0], 0)
		image_starts[-1] = max(image_starts[-1], 0)

		# compute combined image width:
		combined_image_width = sum(digit_image_widths) + sum(image_starts[:-1])
		width_check = max([sum(digit_image_widths[0:i + 1]) + sum(image_starts[0:i + 1])
		                   for i in range(0, num_images)])
		combined_image_width = max(combined_image_width, width_check)

		validate_starts = check_valid_starts(digit_image_widths, image_starts)

		# if image_width is not explicitly defined, use the computed image width as the final image width
		if image_width == 0 and not validate_starts:
			image_width = combined_image_width

	# create combined image numpy array:
	combined_image = np.zeros((IMG_HEIGHT, image_width))
	# set first digit image start:
	start = image_starts[0]

	for idx, digit in enumerate(image_array):
		# subset digit image to the proper image extents
		digit = digit[0:IMG_HEIGHT, image_extents[idx][0]:image_extents[idx][1]]
		# copy digit pixels if digit pixel is greater than 0:
		combined_image[0:IMG_HEIGHT, start:start + digit_image_widths[idx]] = \
			np.where(digit > 0, digit, combined_image[0:IMG_HEIGHT, start:start + digit_image_widths[idx]])
		# increment start by width of digit image, offset with the next image start:
		# start += digit_image_widths[idx] + image_starts[idx + 1]
		start += digit_image_widths[idx] + image_starts[idx + 1]
	return combined_image


def check_valid_starts(digit_image_widths, image_starts):
	"""
	:param digit_image_widths: width of digit images
	:param image_starts: randomly generated starting distance of each digit image
	:return: if any starts is less than 0, return False else True
	"""
	valid_starts = digit_image_widths + np.cumsum(image_starts)[:-1] + np.cumsum(image_starts)[1:] \
	               + np.cumsum([0] + digit_image_widths[1:])
	return any(valid_starts < 0)


def check_valid_input_width(input_image_width, digit_image_widths, num_images, min_max_spacing):
	"""
	:param input_image_width: User defined width of the final combined image width
	:param digit_image_widths: an array of digit image widths
	:param num_images: number of digits
	:param min_max_spacing: spacing limits between digits
	:return: boolean flag of whether the input image width is a valid width with the provided digits and spacing limits
	"""
	probable_image_width = num_images * (np.mean(digit_image_widths) + np.mean(min_max_spacing))
	if input_image_width < probable_image_width > 0:
		warnings.warn(f'Provided combination of digit sequence and spacing cannot fit into image width\n'
		              f'Probable calculated image width = {probable_image_width}')
		return False
	return True


def calculate_img_extent(img, tight):
	"""
	:param img: digit image
	:param tight: calculate image extent from significant pixels in digit image
	:return: minimum, maximum x-axis position of significant pixels in digit image
	"""
	if not tight:
		return 0, img.shape[1]
	min_x = img.shape[1]
	max_x = 0
	for x in range(img.shape[1]):
		for y in range(img.shape[0]):
			if img[y, x] > 0:
				if x < min_x:
					min_x = x
				if x > max_x:
					max_x = x
	assert min_x < max_x
	max_x = min(max_x + 1, img.shape[1])
	min_x = max(min_x - 1, 0)
	return min_x, max_x