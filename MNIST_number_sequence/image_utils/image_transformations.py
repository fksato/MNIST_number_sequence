import numpy as np


def skew(img):
	dl = np.random.randint(50)
	h, l = img.shape
	b = np.zeros((h, l + dl), dtype=img.dtype)
	for y in range(h):
		dec = (dl * (h - y)) // h
		b[y, dec:dec + l] = img[y, :]
	return b