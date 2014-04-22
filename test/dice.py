#!/usr/bin/env python

import random

def d(size):
    return random.randint(1, size)

results = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
cumulative         = 0
percent            = 0.0
cumulative_percent = 0.0

for i in range(100000):
    dice = d(10) + d(10)

    if results[dice] == 0:
        results[dice] = 1
    else:
        results[dice] += 1

index = 20

while results[index]:
    cumulative += results[index]
    
    percent             = results[index] / 1000.0
    cumulative_percent += percent
    print("%2d: %6d (%3.2f - %3.2f)" % (index, results[index],
                                        percent, cumulative_percent))

    index -= 1
