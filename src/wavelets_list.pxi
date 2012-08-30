# Copyright (c) 2006-2012 Filip Wasilewski <http://en.ig.ma/>
# See COPYING for license details.

## Mapping of wavelet names to the C backend codes

cdef __wname_to_code
__wname_to_code = {
    "haar": (c"h", 0),
    
    "db1": (c"d", 1),
    "db2": (c"d", 2),
    "db3": (c"d", 3),
    "db4": (c"d", 4),
    "db5": (c"d", 5),
    "db6": (c"d", 6),
    "db7": (c"d", 7),
    "db8": (c"d", 8),
    "db9": (c"d", 9),
    
    "db10": (c"d", 10),
    "db11": (c"d", 11),
    "db12": (c"d", 12),
    "db13": (c"d", 13),
    "db14": (c"d", 14),
    "db15": (c"d", 15),
    "db16": (c"d", 16),
    "db17": (c"d", 17),
    "db18": (c"d", 18),
    "db19": (c"d", 19),
    "db20": (c"d", 20),
    
    "sym2": (c"s", 2),
    "sym3": (c"s", 3),
    "sym4": (c"s", 4),
    "sym5": (c"s", 5),
    "sym6": (c"s", 6),
    "sym7": (c"s", 7),
    "sym8": (c"s", 8),
    "sym9": (c"s", 9),
    
    "sym10": (c"s", 10),
    "sym11": (c"s", 11),
    "sym12": (c"s", 12),
    "sym13": (c"s", 13),
    "sym14": (c"s", 14),
    "sym15": (c"s", 15),
    "sym16": (c"s", 16),
    "sym17": (c"s", 17),
    "sym18": (c"s", 18),
    "sym19": (c"s", 19),
    "sym20": (c"s", 20),

    "coif1": (c"c", 1),
    "coif2": (c"c", 2),
    "coif3": (c"c", 3),
    "coif4": (c"c", 4),
    "coif5": (c"c", 5),

    "bior1.1": (c"b", 11),
    "bior1.3": (c"b", 13),
    "bior1.5": (c"b", 15),
    "bior2.2": (c"b", 22),
    "bior2.4": (c"b", 24),
    "bior2.6": (c"b", 26),
    "bior2.8": (c"b", 28),
    "bior3.1": (c"b", 31),
    "bior3.3": (c"b", 33),
    "bior3.5": (c"b", 35),
    "bior3.7": (c"b", 37),
    "bior3.9": (c"b", 39),
    "bior4.4": (c"b", 44),
    "bior5.5": (c"b", 55),
    "bior6.8": (c"b", 68),

    "rbio1.1": (c"r", 11),
    "rbio1.3": (c"r", 13),
    "rbio1.5": (c"r", 15),
    "rbio2.2": (c"r", 22),
    "rbio2.4": (c"r", 24),
    "rbio2.6": (c"r", 26),
    "rbio2.8": (c"r", 28),
    "rbio3.1": (c"r", 31),
    "rbio3.3": (c"r", 33),
    "rbio3.5": (c"r", 35),
    "rbio3.7": (c"r", 37),
    "rbio3.9": (c"r", 39),
    "rbio4.4": (c"r", 44),
    "rbio5.5": (c"r", 55),
    "rbio6.8": (c"r", 68),

    "dmey": (c"m", 0),
}

## Lists of family names

cdef __wfamily_list_short, __wfamily_list_long
__wfamily_list_short = ["haar", "db", "sym", "coif", "bior", "rbio", "dmey"]
__wfamily_list_long = ["Haar", "Daubechies", "Symlets", "Coiflets", "Biorthogonal", "Reverse biorthogonal", "Discrete Meyer (FIR Approximation)"]
