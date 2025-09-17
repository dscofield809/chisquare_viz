import matplotlib.pyplot as plt
from matplotlib.widgets import Button, Slider, RadioButtons
from matplotlib.gridspec import GridSpec
import numpy as np
from scipy.stats import chi2_contingency
from scipy.stats import chi2 as chi2_dist

#######################################################################

# This modification of main.py examines a situation in which two variables A and B
# may be related, but we're unsure of the causal direction.
# From a population of N individuals, we collect a sample that is balanced with respect
# to A, and perform a chi square test to see if A and B are independent. 
# We then do the same with a sample that is balanced with respect to B and compare the results. 
# In both cases, we use the largest possible balanced sample.

#######################################################################