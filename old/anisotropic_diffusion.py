import numpy as np
from math import exp

# % ANISODIFF - Anisotropic diffusion.
# %
# % Usage:
# %  diff = anisodiff(im, niter, kappa, lambda, option)
# %
# % Arguments:
# %         im     - input image
# %         niter  - number of iterations.
# %         kappa  - conduction coefficient 20-100 ?
# %         lambda - max value of .25 for stability
# %         option - 1 Perona Malik diffusion equation No 1
# %                  2 Perona Malik diffusion equation No 2
# %
# % Returns:
# %         diff   - diffused image.
# %
# % kappa controls conduction as a function of gradient.  If kappa is low
# % small intensity gradients are able to block conduction and hence diffusion
# % across step edges.  A large value reduces the influence of intensity
# % gradients on conduction.
# %
# % lambda controls speed of diffusion (you usually want it at a maximum of
# % 0.25)
# %
# % Diffusion equation 1 favours high contrast edges over low contrast ones.
# % Diffusion equation 2 favours wide regions over smaller ones.

# % Reference:
# % P. Perona and J. Malik.
# % Scale-space and edge detection using ansotropic diffusion.
# % IEEE Transactions on Pattern Analysis and Machine Intelligence,
# % 12(7):629-639, July 1990.
# %
# % Peter Kovesi
# % School of Computer Science & Software Engineering
# % The University of Western Australia
# % pk @ csse uwa edu au
# % http://www.csse.uwa.edu.au
# %
# % June 2000  original version.
# % March 2002 corrected diffusion eqn No 2.


def anisodiff(im, niter, kappa, gamma, option):

    [nrows, ncols] = im.shape
    diff = im

    for i in range(niter):
        # construct diffl which is the same as diff but has an extra padding of zeros around it
        diffl = np.zeros((nrows + 2, ncols + 2))

        diffl[1:nrows + 1, 1: ncols + 1] = diff

        # North, South, East and West differences
        deltaN = diffl[0:nrows, 1:ncols + 1] - diff
        deltaS = diffl[2:nrows + 2, 1:ncols + 1] - diff
        deltaE = diffl[1:nrows + 1, 2:ncols + 2] - diff
        deltaW = diffl[1:nrows + 1, 0:ncols] - diff

        # Conduction
        if option == 1:
            cN = np.exp(np.power(-(deltaN/kappa), 2))
            cS = np.exp(np.power(-(deltaS/kappa), 2))
            cE = np.exp(np.power(-(deltaE/kappa), 2))
            cW = np.exp(np.power(-(deltaW/kappa), 2))
        elif option == 2:
            cN = np.divide(1, (1 + np.power((deltaN/kappa), 2)))
            cS = np.divide(1, (1 + np.power((deltaS/kappa), 2)))
            cE = np.divide(1, (1 + np.power((deltaE/kappa), 2)))
            cW = np.divide(1, (1 + np.power((deltaW/kappa), 2)))

        diff = diff + gamma * \
            (np.multiply(cN, deltaN) + np.multiply(cS, deltaS) +
             np.multiply(cE, deltaE) + np.multiply(cW, deltaW))

        return diff


def anisodiff_3d(im, niter, kappa, gamma, option):

    [nslices, nrows, ncols] = im.shape
    final_diff = np.copy(im)

    for k in range(nslices):

        diff = im[k]

        for i in range(niter):
            # construct diffl which is the same as diff but has an extra padding of zeros around it
            diffl = np.zeros((nrows + 2, ncols + 2))

            diffl[1:nrows + 1, 1: ncols + 1] = diff

            # North, South, East and West differences
            deltaN = diffl[0:nrows, 1:ncols + 1] - diff
            deltaS = diffl[2:nrows + 2, 1:ncols + 1] - diff
            deltaE = diffl[1:nrows + 1, 2:ncols + 2] - diff
            deltaW = diffl[1:nrows + 1, 0:ncols] - diff

            # Conduction
            if option == 1:
                cN = np.exp(-1 * np.power((deltaN/kappa), 2))
                cS = np.exp(-1 * np.power((deltaS/kappa), 2))
                cE = np.exp(-1 * np.power((deltaE/kappa), 2))
                cW = np.exp(-1 * np.power((deltaW/kappa), 2))
            elif option == 2:
                cN = np.divide(1, (1 + np.power((deltaN/kappa), 2)))
                cS = np.divide(1, (1 + np.power((deltaS/kappa), 2)))
                cE = np.divide(1, (1 + np.power((deltaE/kappa), 2)))
                cW = np.divide(1, (1 + np.power((deltaW/kappa), 2)))

            diff = diff + gamma * \
                (np.multiply(cN, deltaN) + np.multiply(cS, deltaS) +
                 np.multiply(cE, deltaE) + np.multiply(cW, deltaW))

        final_diff[k] = diff

    return final_diff
