#*********************************************************************************
#* Copyright (C) 2016 Kosuke Sato, Alexey V. Akimov
#*
#* This file is distributed under the terms of the GNU General Public License
#* as published by the Free Software Foundation, either version 2 of
#* the License, or (at your option) any later version.
#* See the file LICENSE in the root directory of this distribution
#* or <http://www.gnu.org/licenses/>.
#*
#*********************************************************************************/

## \file moment.py
# This program implements the module that calculates and returns
# the dipole moment matrixes at given space coordinates r like  <MO(t)| r |MO(t+dt)>.
#
# Used in: main.py/main/nve_MD/gamess_to_libra


import os
import sys
import math

# First, we add the location of the library to test to the PYTHON path
sys.path.insert(1,os.environ["libra_mmath_path"])
sys.path.insert(1,os.environ["libra_qchem_path"])

from libmmath import *
from libqchem import *



def transition_dipole_moments(ao,C):
    ##
    # Finds the keywords and their patterns and extracts the parameters
    # \param[in] ao : atomic orbital basis
    # \param[in] C  : MO-LCAO coefficients
    #
    # Used in: main.py/main/nve_MD/gamess_to_libra

    v = VECTOR(0.0,0.0,0.0) # 
    gx = PrimitiveG(1,0,0, 0.0, v) # = x
    gy = PrimitiveG(0,1,0, 0.0, v) # = y
    gz = PrimitiveG(0,0,1, 0.0, v) # = z
    g = [gx,gy,gz]

    Norb = len(ao)
    mu = [MATRIX(Norb, Norb)]*3
    d = MATRIX(Norb,Norb)

    for k in xrange(3): # all components

        # moment matrices in the AO basis
        for i in xrange(Norb): # all orbitals
            for j in xrange(Norb):
                d.set(i,j,gaussian_moment(ao[i], g[k], ao[j]) )
        mu[k] = C.T() * d * C
    
    return mu[0], mu[1], mu[2]