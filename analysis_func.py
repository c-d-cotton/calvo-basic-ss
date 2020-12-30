#!/usr/bin/env python3
import os
from pathlib import Path
import sys

__projectdir__ = Path(os.path.dirname(os.path.realpath(__file__)) + '/')

import matplotlib.pyplot as plt
import numpy as np

def inflation_profitshare():
    Pistar_list = np.linspace(0.99, 1.04, 51)
    Pistar_monthly_list = [Pistar ** (1/12) for Pistar in Pistar_list]
    inflation_list = [100 * (Pistar - 1) for Pistar in Pistar_list]

    profitshare_list = []
    for Pistar in Pistar_monthly_list:
        from calvo-ss_func import calvobasicss
        PstaroverP, MC, NU = calvobasicss(0.96 ** (1/12), 0.087, 8, Pistar)

        profitshare_list.append(100 * (1 - MC * NU))

    plt.plot(inflation_list, profitshare_list)
    plt.xlabel('Annualized Inflation (%)')
    plt.ylabel('Profit Share (%)')

    plt.savefig(__projectdir__ / Path('temp/inflation_profitshare.png'))

    plt.show()

    plt.clf()
        
    
def lambda_pricelevel_partialeq():
    BETA = 0.96 ** (1/12)
    SIGMA = 8
    Pibar = 1.02 ** (1/12)

    def Xbar(LAMBDA):
        X = (1 - (1 - LAMBDA) * BETA * Pibar ** (SIGMA - 1)) / (1 - (1 - LAMBDA) * BETA * Pibar ** SIGMA) * (1 - (1 - LAMBDA) * Pibar ** SIGMA) / (1 - (1 - LAMBDA) * Pibar ** (SIGMA - 1))
        return(X)

    LAMBDA_list = np.linspace(0.05, 0.3, 51)
    Xbar_list = []
    for LABMDA in LAMBDA_list:
        Xbar_list.append(Xbar(LABMDA) - 1)

    plt.plot(LAMBDA_list, Xbar_list)

    plt.xlabel('LAMBDA')
    plt.ylabel('Change in Price Level')

    plt.tight_layout()

    plt.savefig(__projectdir__ / Path('temp/lambda_pricelevel.png'))

    plt.show()

    plt.clf()


# Full:{{{1
def full():
    inflation_profitshare()
    lambda_pricelevel_partialeq()
full()
