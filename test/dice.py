#!/usr/bin/env python

import random

def d(size):
    return random.randint(1, size)

results = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
cumulative         = 0
percent            = 0.0
cumulative_percent = 0.0

for i in range(1000000):
    dice = d(6) + d(6) + d(6)

    if results[dice] == 0:
        results[dice] = 1
    else:
        results[dice] += 1

index = 18

while results[index]:
    cumulative += results[index]
    
    percent             = results[index] / 10000.0
    cumulative_percent += percent
    print("%2d: %5d (%3.2f%% - %3.2f%%)" % (index, results[index],
                                          percent, cumulative_percent))

    index -= 1
