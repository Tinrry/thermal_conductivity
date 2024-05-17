import pandas as pd

def read_txt_and_save_to_csv(txt_file, csv_file):
    df = pd.read_csv(txt_file, delimiter='\t')  
    df.to_csv(csv_file, index=False)

# Example usage
txt_files = ['phi_100.txt', 'y_100.txt']
csv_files = ['phi_100.csv', 'y_100.csv']
for txt_file, csv_file in zip(txt_files, csv_files):
    read_txt_and_save_to_csv(txt_file, csv_file)
    print(f'{txt_file} has been converted to {csv_file}')


import numpy as np
import pandas as pd
import pymc3 as pm
import scipy.stats as stats

# Step 1: Load the material dataset
data = pd.read_csv('material_data.csv')
phi = data['phi'].values
energies = data['energies'].values

# Step 2: Define the prior distributions
with pm.Model() as model:
    weight_phi = pm.Normal('weight_phi', mu=0, sd=10)
    weight_energies = pm.Normal('weight_energies', mu=0, sd=10)
    intercept = pm.Normal('intercept', mu=0, sd=10)

    # Step 3: Define the likelihood function
    mu = intercept + weight_phi * phi + weight_energies * energies
    sigma = pm.HalfNormal('sigma', sd=10)
    likelihood = pm.Normal('likelihood', mu=mu, sd=sigma, observed=data['target'])  # Assuming 'target' is the observed variable

    # Step 4: Calculate the posterior distribution
    trace = pm.sample(1000, return_inferencedata=False)

# Step 5: Estimate the weights
estimated_weight_phi = np.mean(trace['weight_phi'])
estimated_weight_energies = np.mean(trace['weight_energies'])

# Print the estimated weights
print("Estimated weight of phi:", estimated_weight_phi)
print("Estimated weight of energies:", estimated_weight_energies)