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

    # Inference
    trace = pm.sample(2000, tune=1000, cores=1)

# Print the summary of the trace
print(pm.summary(trace))