# GOTCHA
## A tesseract-based method for solving CAPTCHAs

GOTCHA is a python module intended to provide a way for handling [CAPTCHAs](https://en.wikipedia.org/wiki/CAPTCHA) in automated testing. GOTCHA accepts images represented as numpy arrays and returns a character string with its guess. GOTCHA is not meant to be used for bypassing any actual security measures - This is why it will only work with extremely simple CAPTCHAs such as _Simple PHP CAPTCHA_ or the _Really simple CAPTCHA plugin_ for WordPress. 

Once this project is complete, it will feature a method for solving simple CAPTCHAs using the tesseract OCR engine. This project consists of three parts:
- [x] A PHP-Script generating ground truth
- [x] A jupyter notebook containing a description of the methodology and the evaluation
- [x] A python script for CLI that can also be used as a module

## Use
**Requirements**

A working installation of the tesseract ocr engine. To install on Debian/Ubuntu:
```bash
$ sudo apt-get install tesseract-ocr
```
The Python modules listed in requirements.txt. To install them run:

```bash
$ pip3 install -r requirements.txt
```
**Python**

When imported as a python module, captcha_solver.py provides the function solve_captcha() that inputs a CAPTCHA-image and returns a guess of the solution:
```python
solve_captcha(image, deskew=True, pagesegmode=11, verbose=False):
    """
    Receives a CAPTCHA as input, processes it and returns a string with the guess for the solution.
    
    :praram image:      The CAPTCHA represented as ndarray (via cv2.imread)
    :param deskew:      boolean, whether the image schould be deskewed
    :param pagesegmode: int 0-13, page segmentation mode for tesseract
    :param verbose:     boolean, if True, individual steps are being shown
    :return:            string, the CAPTCHA solution
    """
```

**Command line**

```
$ python3 captcha_solver.py ./captcha.png

positional arguments:
  img_path              Input file

optional arguments:
  -h, --help            Show this help message and exit
  --deskew              Should the image be deskewed? (default: True)
  --pagesegmode         Page segmentation mode for tesseract (default: 11)
  --verbose             Show intermediate steps? (default: False)

```

## Evalutation
### Dataset generator
The Dataset generator is a modified version of Yasir M. Türk's [Simple PHP CAPTCHA](https://github.com/yasirmturk/simple-php-captcha), which has been kindly released under the MIT license.

**Requirements:**
* PHP 7
* PHP GD2
* At least one font placed in the "fonts" directory.

If the requirements are not satisfied, you may install PHP as follows (Debian/Ubuntu);
```bash
$ sudo apt-get install php
$ sudo apt-get install php-gd
```


**gotcha.php**

The actual generator: Will save a PNG image in the specified directory, where the filename is the solution of the CAPTCHA.
The script has been adapted to be executable via the command line interface:
```bash
$ php gotcha.php -o ./data -b blank.png -m 3 -x 5
```
Arguments:
* -o:   Output directory
* -b:   Background image (PNG of size 160x75)
* -m:   Minimum length of CAPTCHA
* -x:   Maximum length of CAPTCHA

**build_dataset.sh**

Example shell script generating the datasets used for the project. Callable via CLI:
```bash
$ bash ./build_dataset.sh -n=1000
```
Arguments:
* -n:   Total size of dataset to generate

### Evaluation script

**GOTCHA_concept.ipynb**

This Jupyter notebook includes the entire code of the project and includes additional documentation, as well as evaluation on the ground truth.

### Results
The following results have been obtained by analyzing 1.000 CAPTCHAs per dataset using default settings.



| Dataset                      | Accuracy    |
|------------------------------|-------------|
| Simple PHP CAPTCHA           | 0.658       |
| Really Simple CAPTCHA Plugin | tbd         |
