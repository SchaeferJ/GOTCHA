# GOTCHA
## A tesseract-based method for solving CAPTCHAs

GOTCHA is a python module intended to provide a way for handling [CAPTCHAs](https://en.wikipedia.org/wiki/CAPTCHA) in automated testing. GOTCHA accepts images represented as numpy arrays and returns a character string with its guess. GOTCHA is not meant to be used for bypassing any actual security measures - This is why it will only work with extremely simple captchas such as _Simple PHP CAPTCHA_ or the _Really simple CAPTCHA plugin_ for WordPress. 

Once this project is complete, it will feature a method for solving simple CAPTCHAs using the tesseract OCR engine. This project consists of three parts:
- [x] A PHP-Script generating ground truth
- [x] A jupyter notebook containing a description of the methodology and the evaluation
- [ ] A python script that can be imported as a module

**NOTE: This is an academic proof-of-concept project. It is NOT meant to be used in productive einvironments of any kind. In particular, the code should not be used to circumvent any measures protecting against Spam, DDOS-Attacks or unauthorized access!**

## Dataset generator
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

## Evaluation

**GOTCHA_concept.ipynb**

This Jupyter notebook includes the entire code of the project and includes additional documentation, as well as evaluation on the ground truth.

**Results**
With an accuracy of 66% GOTCHA significantly outperforms the random baseline - A six digit CAPTCHA corresponds to a total of 56,800,235,584 different combinations and is essentially unguessable.

| Dataset                      | Accuracy    |
|------------------------------|-------------|
| Simple PHP CAPTCHA           | 0.66        |
| Really Simple CAPTCHA Plugin | tbd         |
