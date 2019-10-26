#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

Test finding a new design point, thetaT

@author: David P. Fleming [University of Washington, Seattle], 2018
@email: dflemin3 (at) uw (dot) edu

"""

from approxposterior import approx, likelihood as lh, gpUtils
import numpy as np
import george


def test_find():
    """
    Test the findNextPoint function.
    """

    # Define algorithm parameters
    m0 = 50                           # Initial size of training set
    bounds = ((-5,5), (-5,5))         # Prior bounds
    algorithm = "bape"

    # For reproducibility
    seed = 57
    np.random.seed(seed)

    # Randomly sample initial conditions from the prior
    # Note: adding a corner case because approxposterior loves corners
    theta = np.array(list(lh.rosenbrockSample(m0)) + [[-5, 5]])

    # Evaluate forward model log likelihood + lnprior for each theta
    y = np.zeros(len(theta))
    for ii in range(len(theta)):
        y[ii] = lh.rosenbrockLnlike(theta[ii]) + lh.rosenbrockLnprior(theta[ii])

    # Set up a gp
    gp = gpUtils.defaultGP(theta, y)

    # Initialize object using the Wang & Li (2017) Rosenbrock function example
    # using default ExpSquaredKernel GP
    ap = approx.ApproxPosterior(theta=theta,
                                y=y,
                                gp=gp,
                                lnprior=lh.rosenbrockLnprior,
                                lnlike=lh.rosenbrockLnlike,
                                priorSample=lh.rosenbrockSample,
                                bounds=bounds,
                                algorithm=algorithm)

    # Find new point!
    thetaT = ap.findNextPoint(computeLnLike=False,
                              bounds=bounds,
                              seed=seed)

    err_msg = "findNextPoint selected incorrect thetaT."
    assert(np.allclose(thetaT, [1.67465919, -4.99999997], rtol=1.0e-3)), err_msg
# end function

if __name__ == "__main__":
    test_find()
