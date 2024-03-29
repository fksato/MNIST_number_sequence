import pytest


class TestImageUtilsGetDigits:
	@pytest.mark.parametrize(['segment', 'digits', 'expected_image_shape', 'expected_num_images']
							, [ ("train", [1,2,3,4,5], 28, 5)
		                         , ("test", [1,2,3,4,5], 28, 5)])
	def test_get_digits(self, segment, digits, expected_image_shape, expected_num_images):
		from MNIST_number_sequence.mnist_loader import MNISTLoader
		from MNIST_number_sequence.image_utils import get_digits
		from MNIST_number_sequence.image_utils.image_transformations import skew
		MNIST_ds = MNISTLoader(dataset_regime=segment)

		check_extents, check_digits = get_digits(digits, MNIST_ds, tight=False, apply=None)
		for idx in range(len(check_extents)):
			assert check_extents[idx] == (0, expected_image_shape)
		assert len(check_extents) == len(check_digits)
		for img in check_digits:
			assert img.shape == (expected_image_shape, expected_image_shape)
		assert len(check_digits) == expected_num_images

		check_extents, check_digits = get_digits(digits, MNIST_ds, tight=True, apply=None)
		assert len(check_digits) == expected_num_images
		assert len(check_extents) == len(check_digits)

		check_extents, check_digits = get_digits(digits, MNIST_ds, tight=True, apply=skew)
		assert len(check_digits) == expected_num_images
		assert len(check_extents) == len(check_digits)


class TestImageUtilsCombineImages:
	@pytest.mark.parametrize(['segment', 'digits', 'digit_spacing', 'image_width', 'expected_image_width'
	                        , 'check_img_width_limit']
							, [('train', [1,2,3,4,5,6], (-10,10), 200, 200, True)
							   , ('train', [1,2,3,4,5,6], (-90,0), 0, None, False)
							   , ('test', [1,2,3,4,5,6], (-10,10), 200, 200, True)])
	def test_combine_images(self, segment, digits, digit_spacing, image_width, expected_image_width
	                        , check_img_width_limit):
		from MNIST_number_sequence.mnist_loader import MNISTLoader
		from MNIST_number_sequence.image_utils import get_digits, combine_images
		from MNIST_number_sequence.image_utils.image_transformations import skew
		MNIST_ds = MNISTLoader(dataset_regime=segment)

		test_img_extents, test_img_array = get_digits(digits, MNIST_ds, tight=False, apply=None)
		test_combined = combine_images(test_img_array, test_img_extents, digit_spacing, image_width=image_width)

		if image_width is not None and image_width != 0:
			assert test_combined.shape[1] == expected_image_width

		test_img_extents, test_img_array = get_digits(digits, MNIST_ds, tight=True, apply=skew)
		combine_images(test_img_array, test_img_extents, digit_spacing, image_width=None)

		if check_img_width_limit:
			with pytest.raises(Exception):
				combine_images(test_img_array, test_img_extents, digit_spacing, image_width=1)

		test_img_extents, test_img_array = get_digits(digits, MNIST_ds, tight=True, apply=None)
		combine_images(test_img_array, test_img_extents, digit_spacing, image_width=None)

		test_img_extents, test_img_array = get_digits(digits, MNIST_ds, tight=True, apply=skew)
		combine_images(test_img_array, test_img_extents, digit_spacing, image_width=None)
