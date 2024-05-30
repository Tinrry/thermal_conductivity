import pandas as pd
import pymc3 as pm

# Read the data from data.csv
data = pd.read_csv('./data_20240529.csv', header=0)

# Define the variables
x = data[['phi_0', 'phi_1', 'phi_2', 'phi_3', 'phi_4', 'phi_5', 'phi_6', 'phi_7', 
          'phi_8', 'phi_9', 'phi_10', 'phi_11', 'phi_12', 'phi_13', 'phi_14', 'phi_15', 'phi_16', 'phi_17']]
y = data['energy']
print(x.describe())

# Create a PyMC3 model
with pm.Model() as model:
    # Priors for the coefficients
    alpha = pm.Normal('alpha', mu=0, sd=10)
    beta = pm.Normal('beta', mu=0, sd=10, shape=len(x.columns))

    # Linear regression model
    mu = alpha + pm.math.dot(beta, x.T)

    # Likelihood
    sigma = pm.HalfNormal('sigma', sd=1)
    likelihood = pm.Normal('y', mu=mu, sd=sigma, observed=y)

    # Load the trace from the file
    trace = pm.load_trace('trace')

    # Inference
    # 通过增加 tune 参数的值来增加调优步骤的数量。调优步骤在实际采样开始之前进行，用于调整采样器的参数以提高采样效率。
    trace = pm.sample(2000, tune=5000, cores=1, target_accept=0.9,
                      start=trace.points[-1] if 'trace' in locals() else None)

# get beta sd and sigma sd from the trace
beta_sd = trace['beta'].std(axis=0)
sigma_sd = trace['sigma'].std()
print('beta_sd: ', beta_sd)
print('sigma_sd: ', sigma_sd)

# # Print the summary of the trace
# print(pm.summary(trace))

# Save the trace to a file
pm.save_trace(trace, 'trace')


# trace_df = pm.trace_to_dataframe(trace)
# trace_df.to_csv('trace.csv', index=False)

# import matplotlib.pyplot as plt

# # Plot the trace
# pm.traceplot(trace)
# plt.show()

# # Plot the posterior distribution
# pm.plot_posterior(trace)
# plt.show()

# # Plot the posterior distribution of the coefficients
# pm.plot_posterior(trace, var_names=['alpha', 'beta'])
# plt.show()

from utils import get_parameters_variance
variance = get_parameters_variance(x,  beta_sd, sigma_sd)
