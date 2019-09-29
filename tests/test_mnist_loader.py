import pytest

class TestMNISTLoader:
	@pytest.mark.parametrize(['segment', 'expected_records_count', 'image_size']
							, [ ("train", 60000, 28)
								, ("test", 10000, 28)])
	def test_create_MNIST_ds(self, segment, expected_records_count, image_size):
		from MNIST_number_sequence.mnist_loader import MNISTLoader

		MNIST_ds = MNISTLoader(dataset_regime=segment)
		assert len(list(MNIST_ds.digit_hash.keys())) == 10

		data_cnt = sum([len(MNIST_ds.digit_hash[key]) for key in MNIST_ds.digit_hash.keys()])
		assert data_cnt == expected_records_count

		for i in MNIST_ds.digit_hash.keys():
			img = MNIST_ds.get_digit_image(i)
			assert img.shape == (image_size, image_size)

