This is a Python implementation of a radix packing compression technique which we refer to as Bignum. We show that Bignum is similar to and at times better than prior published state of the art integer compression techniques in terms of bits per integer.

This code is written for Python 2.7, and tested only on Unix-like operating systems, specifically OS X, and Ubuntu.

Usage
-----

The basic command to run a comparitive study of different compression techniques::

    ./main.py -i $target_name.csv 

Since the current work is focused on polygons from `DHS <https://www.fema.gov/frequently-asked-questions-wireless-emergency-alerts/>`_, the format of the csv file is based on the data file found here `WEA polygons <https://drive.google.com/file/d/0BwHlzpAMFkx6SWhKUkFFdTY4emc/view?usp=sharing>`_.

Aggregated results after the execution of ``main.py`` can be found under the ``results`` folder in csv files.

Plots can be generated post running the ``main.py`` by::

    ./comparison_plots.py
    
Comparison
----------

For comparison purposes, we considered `TurboPFor <https://github.com/powturbo/TurboPFor>`_ (cloned on October 25, 2015) executed using::

    ./icbench $input_file -f1

Since the above takes a long time to run, you can view the results for each of polygon under the folder ``results/delta_min_state_of_art``  and ``results/delta_state_of_art``. Each filename corresponds to an identification between 1 & 11,370.

Separate file for each polygon as input to ``icbench`` can be taken from folders ``delta_min_polygons`` and ``delta_polygons``. A file for each polygon is generated after running ``main.py``.

Publications
------------
* [Poster](http://abhinavjauhri.com/publications/dcc_poster_2016.pdf)
* [Paper] (http://arxiv.org/abs/1509.05505)
