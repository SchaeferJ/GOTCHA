# GOTCHA
## A neural-network-based method for solving CAPTCHAs

Once this project is complete, it will feature a method for solving simple CAPTCHAs using neural networks. This project consist of two parts:
- [x] A PHP-Script generating ground truth
- [ ] A neural network

**NOTE: This is an academic proof-of-concept project. It is NOT meant to be used in productive einvironments of any kind. In particular, the code should not be used to circumvent any measures protecting against Spam, DDOS-Attacks or unauthorized access!**

## Dataset generator
The Dataset generator is a modified version of Yasir M. Türk's [Simple PHP CAPTCHA](https://github.com/yasirmturk/simple-php-captcha), which has been kindly released under the MIT license.

**Requirements:**
* PHP 7
* PHP GD2
If the requirements are not satisfied, you may install them as follows (Debian/Ubuntu);
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
$ bash ./build_dataset.sh -n=1000 -s=80 -v
```
Arguments:
* -n:   Total size of dataset to generate
* -s:   Size of training set (a value of 80 will result in 80% training and 20% test data)
* -v:   If set, the script produces an extra validation set the size of the test set
