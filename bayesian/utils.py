import numpy as np


def get_parameters_variance(big_phi, beta, sigma):
    # 实现公式21， beta sd, sigma sd and x data get variance the uncertainty of the parameters.
    big_phiT_phi = np.dot(big_phi.T, big_phi) / sigma ** 2
    identity_matrix_over_beta_variance = np.eye(beta.shape[0]) / beta ** 2
    variance = np.linalg.inv(identity_matrix_over_beta_variance + big_phiT_phi)
    # save variance to csv, can overwire the file.
    np.savetxt('variance.csv', variance, delimiter=',')
    return variance

if __name__ == "__main__":
    big_phi = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12], [13, 14, 15]])
    beta = np.array([1, 2, 3])
    sigma = 0.5
    print(get_parameters_variance(big_phi, beta, sigma))
# [[ 0.494974   -0.91516981  0.42696986]
#  [-0.91516981  1.94345119 -1.01794139]
#  [ 0.42696986 -1.01794139  0.57653498]]