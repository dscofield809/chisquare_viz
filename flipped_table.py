import matplotlib.pyplot as plt
from matplotlib.widgets import Button, Slider, RadioButtons
from matplotlib.gridspec import GridSpec
import numpy as np
from scipy.stats import chi2_contingency
from scipy.stats import chi2 as chi2_dist

#######################################################################

# This modification of main.py examines a situation in which two variables A and B
# may be related, but we're unsure of the causal direction.
# From a population, we collect a sample that is balanced with respect to A, and 
# perform a chi square test to see if A and B are independent. 
# We then do the same with a sample that is balanced with respect to B and compare the results. 
# In both cases, we use the largest possible balanced sample.

# Setup:
# Population with two variables: treatment and recovery
# Proportion of population treated: 0.30
# Proportion of population recovered: 0.45

# Proportion of population treated (recovered: 0.15, not: 0.15)
# Proportion of population not treated: (recovered: 0.30, not: 0.40)

# A. Imaginary random sample balanced for treatment:
# Include all treated and 30/70 of untreated (each 0.30 of total)
# Proportion of sample treated and recovered: 0.25 (not rec: 0.25)
# Suppose: Proportion of sample not treated and recovered: ?? (not rec: ??)

# B. Imaginary random sample balanced for recovery:
# Include all recovered and 45/55 of unrecovered (each 0.45 of total)
# Proportion of sample treated and recovered: 15/90 (not rec: ??)
# Suppose: Proportion of sample not treated and recovered: 30/90 (not rec: ??)


#######################################################################