# Copyright (c) 2018, Abhinav Jauhri, Martin Griss, Hakan Erdogmus
# All rights reserved.
# Licensed under the BSD 3-Clause license.
# For full license text, see the LICENSE file in the repo root

# Info about compression algo: http://en.wikipedia.org/wiki/Lempel%E2%80%93Ziv%E2%80%93Markov_chain_algorithm 
# Installed from https://github.com/fancycode/pylzma/   
import pylzma
def encode(coords):
    encoding = pylzma.compress(s)
    return encoding
