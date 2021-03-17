#!/usr/bin/env python3
import os
from pathlib import Path
import sys

__projectdir__ = Path(os.path.dirname(os.path.realpath(__file__)) + '/')


def calvobasicss(BETA, LAMBDA, SIGMA, Pistar):
    if (1 - (1 - LAMBDA) / Pistar**(1 - SIGMA)) <= 0:
        print(1 - (1 - LAMBDA) / Pistar**(1 - SIGMA))
        raise ValueError('Not possible to define PstaroverP')
    PstaroverP = ((1 - (1 - LAMBDA) / Pistar**(1 - SIGMA))/LAMBDA)**(1/(1 - SIGMA))
    MC = (SIGMA - 1)/SIGMA * (1 - (1 - LAMBDA) * BETA * Pistar ** SIGMA) / (1 - (1 - LAMBDA) * BETA * Pistar ** (SIGMA - 1)) * PstaroverP
    NU = 1/(1 - (1 - LAMBDA) * Pistar**SIGMA) * LAMBDA * PstaroverP ** (-SIGMA)

    return(PstaroverP, MC, NU)


