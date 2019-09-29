# MNIST Number Sequence Generator
### Generate a sequence of handwritten numbers using MNIST data

### Main modules
* mnist_loader
    
    MNIST data repository. Handles downloading, loading, and organizing MNIST digt images
    
* image_utils

    MNIST digit image utility libraries used to aggregate, transform, and combine into a 
    single image
 
##### Config
* Designates ROOT_DIR, where all MNIST dataset I/O operations occur
* Creates "dataset" directory where MNIST datasets are stored
 
### Installation

```
pip install "MNIST_number_generator @ git+https://github.com/fksato/MNIST_number_sequence"
```

### Requirements
* python >= 3.6
* numpy >= 1.16.4
* pillow >= 6.1.0

_All requirements will be met automatically when pip installed_

### Usage
Loading MNIST dataset
```python
from MNIST_number_sequence.mnist_loader import MNISTLoader
MNIST_dataset = MNISTLoader(segment="train")
```
segment can be either "train" or "test" and will load the respective MNIST image and label 
dataset

MNISTLoader object will create a hash table which can be used to query the MNIST dataset
 for specific digits
```python
MNIST_dataset.get_digit_image(digit=2)
```
Users may also choose to get an image from the dataset at an arbitrary index
```python
MNIST_dataset.get_image_at(idx=532)
```
The return type of these functions are an uint8 numpy ndarray of size [28, 28]

## Generating a sequence of numbers
Users can generate an image of a sequence of digit images from MNIST dataset by either 
utilizing the __image_utils__ library, or by using the __generate_sequence.py__ convenience 
script.

### Using the __generate_sequence.py__ convenience script
Users can use the __generate_sequence.py__ by invoking it from a command-line terminal.
To get help in the available options call:
```bash
python generate_sequence.py -h
```
__generate_sequence.py__ 
* __-d, --digits__: a sequence of numbers to generate an image. Each digit in the sequence 
should be separated by a space and can only be single digit number found in MNIST. 
(cannot be a number less than 0 or larger than 9)
* __-s, --spacing_range__: two numbers that represents the minimum/maximum allowable spacing 
between each digit. The two numbers must be separated by a space. Order of the numbers must 
be __minimum first__ then the maximum allowable spacing.
* __-w, --image_width__: An optional flag which the user can explicitly set the image width of 
the final combined image. (default=None)
**_care should be taken to specify a large enough image width to accomodate the number of 
digits and the spacing between each digit_
* __--dataset_regime__: An optional string parameter that specifies which MNIST 
dataset to retrieve from. Options include: __"train"__ or __"test"__. (default="train")
* _--image_save_name__: An optional string parameter which the user may use to specify the
 file name of the final combined image. (default="combined_sequence.png")
 
__Example__:
```bash
python generate_numbers_sequence.py -d 1 2 3 4 5 -s -10 10 -w 150 --dataset_regime "testing" --image_save_name "combined_12345.png"
```

### Using the __image_utils__ library
Users can get retreive a list of digit images from the MNISTLoader by calling the 
__get_digits__ function
```python
from MNIST_number_sequence.image_utils import get_digits, combine_images
image_extents, digit_images = get_digits(digits=[1,2,3,4,5], MNIST_dataset)
```
___
__get_digits(digits, mnist_images_ds, tight=False, apply=None)__

* __digits__: a desired sequence of integers between 0-9 as a list
* __mnist_images_ds__: MNISTLoader object
* __tight__: (default=False) prescribes how to calculate the extents of the digit image
-- By default the extents of the digit images are calculated using the bounding box of the 
digit image. Otherwise, the minimum/maximum x positon of non-zero pixel value is used.
* __apply__: (default=None) An optional field that applies an image transformation on 
th digit image. _Currently, __skew__ is the only image transformation that is implemented._
___

With the sequence of digit images and their extents, users can generate a single image 
by invoking the __combine_images__ function.
___
```python
min_max_spacing = (-10, 10)
image_width = 145
combine_images(digit_images, image_extents, min_max_spacing, image_width)
```
__combine_images(image_array, image_extents, min_max_spacing, image_width=None)__

* __image_array__: a list of digit images
* __image_extents__: a list of tuples that correspond to the minimum/maximum extents of 
each digit image in the image array
* __min_max_spacing__: a tuple that represents the minimum/maximum allowable spacing between 
each digit in the final combined image
* __image_width__: (default=None) an optional parameter which the user may use to specify 
the final width of the combined image

**_care should be taken to specify a large enough image width to accomodate the number of 
digits and the spacing between each digit_
___
__combine_images__ will return a single uint8 numpy ndarray that represents the sequence 
of digit images as a single image.

At this step, the user may choose to do as they wish with the image array. To save the image,
 the user can use a library such as pillow, which is included in this package.