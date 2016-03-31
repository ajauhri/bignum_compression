This is a Python implementation of a radix packing compression technique which we refer to as Bignum. We show that Bignum is similar to and at times better than prior published state of the art integer compression techniques in terms of bits per integer.

This code is written for Python 2.7, and tested only on Unix-like operating systems, specifically OS X, and Ubuntu.

Usage
-----

The basic command to run a comparitive study of different compression techniques::

    ./main.py -i $target_name.csv 

Since the current work is focused on polygons from `DHS <https://www.fema.gov/frequently-asked-questions-wireless-emergency-alerts/>`_, the format of the csv file is based on the data file found here `WEA polygons <https://drive.google.com/file/d/0BwHlzpAMFkx6SWhKUkFFdTY4emc/view?usp=sharing>`_.

Comparison
----------

For comparison purposes, we considered `TurboPFor <https://github.com/powturbo/TurboPFor>`_ (cloned on October 25, 2015) executed using::

    ./icbench <filename> -f1

Since the above takes a long time to run, you can view the results for each of polygon under the folder ``results/del_state_of_art`` 

