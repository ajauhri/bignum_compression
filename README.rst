This is a Python implementation of a radix packing compression technique which we refer to as Bignum. We show that Bignum is similar to and at times better than prior published state of the art integer compression techniques in terms of bits per integeru

This code is written for Python 2.7, and tested only on Unix-like operating systems, specifically OS X, and Ubuntu.

Usage
-----

The basic command to run a comparitive study of different compression techniques::

    ./main.py -i $target_name.csv 

Since the current work is focused on polygons from `DHS <https://www.fema.gov/frequently-asked-questions-wireless-emergency-alerts/>`_, the format of the csv file is based on the data file found here `WEA polygons `_.

