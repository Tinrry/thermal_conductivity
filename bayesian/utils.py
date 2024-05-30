import numpy as np


def get_parameters_variance(big_phi, beta, sigma):
    # 实现公式21， beta sd, sigma sd and x data get variance the uncertainty of the parameters.
    big_phiT_phi = np.dot(big_phi.T, big_phi) / sigma ** 2
    identity_matrix_over_beta_variance = np.eye(beta.shape) / beta ** 2
    variance = np.linalg.inv(identity_matrix_over_beta_variance + big_phiT_phi)
    return variance
