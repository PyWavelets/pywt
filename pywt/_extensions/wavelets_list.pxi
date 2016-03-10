# Copyright (c) 2006-2012 Filip Wasilewski <http://en.ig.ma/>
# See COPYING for license details.

## Mapping of wavelet names to the C backend codes

cdef __wname_to_code
__wname_to_code = {
    "haar": (0, 0),
    
    "db1": (2, 1),
    "db2": (2, 2),
    "db3": (2, 3),
    "db4": (2, 4),
    "db5": (2, 5),
    "db6": (2, 6),
    "db7": (2, 7),
    "db8": (2, 8),
    "db9": (2, 9),
    
    "db10": (2, 10),
    "db11": (2, 11),
    "db12": (2, 12),
    "db13": (2, 13),
    "db14": (2, 14),
    "db15": (2, 15),
    "db16": (2, 16),
    "db17": (2, 17),
    "db18": (2, 18),
    "db19": (2, 19),
    
    "db20": (2, 20),
    "db21": (2, 21),
    "db22": (2, 22),
    "db23": (2, 23),
    "db24": (2, 24),
    "db25": (2, 25),
    "db26": (2, 26),
    "db27": (2, 27),
    "db28": (2, 28),
    "db29": (2, 29),
    
    "db30": (2, 30),
    "db31": (2, 31),
    "db32": (2, 32),
    "db33": (2, 33),
    "db34": (2, 34),
    "db35": (2, 35),
    "db36": (2, 36),
    "db37": (2, 37),
    "db38": (2, 38),
    
    "sym2": (3, 2),
    "sym3": (3, 3),
    "sym4": (3, 4),
    "sym5": (3, 5),
    "sym6": (3, 6),
    "sym7": (3, 7),
    "sym8": (3, 8),
    "sym9": (3, 9),
    
    "sym10": (3, 10),
    "sym11": (3, 11),
    "sym12": (3, 12),
    "sym13": (3, 13),
    "sym14": (3, 14),
    "sym15": (3, 15),
    "sym16": (3, 16),
    "sym17": (3, 17),
    "sym18": (3, 18),
    "sym19": (3, 19),
    "sym20": (3, 20),

    "coif1": (4, 1),
    "coif2": (4, 2),
    "coif3": (4, 3),
    "coif4": (4, 4),
    "coif5": (4, 5),
    "coif6": (4, 6),
    "coif7": (4, 7),
    "coif8": (4, 8),
    "coif9": (4, 9),
    
    "coif10": (4, 10),
    "coif11": (4, 11),
    "coif12": (4, 12),
    "coif13": (4, 13),
    "coif14": (4, 14),
    "coif15": (4, 15),
    "coif16": (4, 16),
    "coif17": (4, 17),


    "bior1.1": (5, 11),
    "bior1.3": (5, 13),
    "bior1.5": (5, 15),
    "bior2.2": (5, 22),
    "bior2.4": (5, 24),
    "bior2.6": (5, 26),
    "bior2.8": (5, 28),
    "bior3.1": (5, 31),
    "bior3.3": (5, 33),
    "bior3.5": (5, 35),
    "bior3.7": (5, 37),
    "bior3.9": (5, 39),
    "bior4.4": (5, 44),
    "bior5.5": (5, 55),
    "bior6.8": (5, 68),

    "rbio1.1": (1, 11),
    "rbio1.3": (1, 13),
    "rbio1.5": (1, 15),
    "rbio2.2": (1, 22),
    "rbio2.4": (1, 24),
    "rbio2.6": (1, 26),
    "rbio2.8": (1, 28),
    "rbio3.1": (1, 31),
    "rbio3.3": (1, 33),
    "rbio3.5": (1, 35),
    "rbio3.7": (1, 37),
    "rbio3.9": (1, 39),
    "rbio4.4": (1, 44),
    "rbio5.5": (1, 55),
    "rbio6.8": (1, 68),

    "dmey": (6, 0),
    
    "gaus1": (7, 1),
    "gaus2": (7, 2),
    "gaus3": (7, 3),
    "gaus4": (7, 4),
    "gaus5": (7, 5),
    "gaus6": (7, 6),
    "gaus7": (7, 7),
    "gaus8": (7, 8),
    
    "mexh": (8, 0),
    
    "morl": (9, 0),
    
    "cgau1": (10, 1),
    "cgau2": (10, 2),
    "cgau3": (10, 3),
    "cgau4": (10, 4),
    "cgau5": (10, 5),
    "cgau6": (10, 6),
    "cgau7": (10, 7),
    "cgau8": (10, 8),
    
    "shan": (11, 0),
    
    "fbsp": (12, 0),
    
    "cmor": (13, 0),
}

## Lists of family names

cdef __wfamily_list_short, __wfamily_list_long
__wfamily_list_short = ["haar", "db", "sym", "coif", "bior", "rbio", "dmey", "gaus", "mexh", "morl", "cgau", "shan", "fbsp", "cmor"]
__wfamily_list_long = ["Haar", "Daubechies", "Symlets", "Coiflets", "Biorthogonal", "Reverse biorthogonal", "Discrete Meyer (FIR Approximation)", "Gaussian", "Mexican hat wavelet", "Morlet wavelet", "Complex Gaussian wavelets", "Shannon wavelets", "Frequency B-Spline wavelets",  "Complex Morlet wavelets"]
