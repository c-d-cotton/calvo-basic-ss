#!/usr/bin/env python3
# PYTHON_PREAMBLE_START_STANDARD:{{{

# Christopher David Cotton (c)
# http://www.cdcotton.com

# modules needed for preamble
import importlib
import os
from pathlib import Path
import sys

# Get full real filename
__fullrealfile__ = os.path.abspath(__file__)

# Function to get git directory containing this file
def getprojectdir(filename):
    curlevel = filename
    while curlevel is not '/':
        curlevel = os.path.dirname(curlevel)
        if os.path.exists(curlevel + '/.git/'):
            return(curlevel + '/')
    return(None)

# Directory of project
__projectdir__ = Path(getprojectdir(__fullrealfile__))

# Function to call functions from files by their absolute path.
# Imports modules if they've not already been imported
# First argument is filename, second is function name, third is dictionary containing loaded modules.
modulesdict = {}
def importattr(modulefilename, func, modulesdict = modulesdict):
    # get modulefilename as string to prevent problems in <= python3.5 with pathlib -> os
    modulefilename = str(modulefilename)
    # if function in this file
    if modulefilename == __fullrealfile__:
        return(eval(func))
    else:
        # add file to moduledict if not there already
        if modulefilename not in modulesdict:
            # check filename exists
            if not os.path.isfile(modulefilename):
                raise Exception('Module not exists: ' + modulefilename + '. Function: ' + func + '. Filename called from: ' + __fullrealfile__ + '.')
            # add directory to path
            sys.path.append(os.path.dirname(modulefilename))
            # actually add module to moduledict
            modulesdict[modulefilename] = importlib.import_module(''.join(os.path.basename(modulefilename).split('.')[: -1]))

        # get the actual function from the file and return it
        return(getattr(modulesdict[modulefilename], func))

# PYTHON_PREAMBLE_END:}}}

import matplotlib.pyplot as plt
import numpy as np

def inflation_profitshare():
    Pistar_list = np.linspace(0.99, 1.04, 51)
    Pistar_monthly_list = [Pistar ** (1/12) for Pistar in Pistar_list]
    inflation_list = [100 * (Pistar - 1) for Pistar in Pistar_list]

    profitshare_list = []
    for Pistar in Pistar_monthly_list:
        PstaroverP, MC, NU = importattr(__projectdir__ / Path('calvo-ss_func.py'), 'calvobasicss')(0.96 ** (1/12), 0.087, 8, Pistar)

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
