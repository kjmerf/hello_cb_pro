import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import statsmodels as sm
from statsmodels.tsa.statespace.mlemodel import MLEModel


# Read in data
df = pd.read_json("/tmp/cb_pro.json", lines=True)
df.to_csv("/tmp/bitcoin.csv", index=False)

# Process with analysis.R and come back
daily = pd.read_csv("/tmp/daily-bitcoin.csv")

class MomentumFilter(MLEModel):
    param_names = ['sigma_a', 'sigma_e']
    start_params = [.001, .0011]

    def __init__(self, logprice):
        initial = logprice[0]
        super().__init__(logprice[1:], k_states=2)

        self.initialize_known(np.array([initial, 0]), np.eye(2))

    def update(self, params, **kwargs):
        params = super().update(params, **kwargs)
        
        self['transition'] = np.array([[1, 1], [0, 1]])

        # premultiplied by state vector
        self['design'] = np.array([1, 0])

        # premultiplied by state error
        self['selection'] = np.diag([1, 1])

        self['state_cov'] = np.diag([params[1] ** 2, params[0] ** 2])

        self['obs_intercept', 0, 0] = 0
        self['obs_cov', 0, 0] = 0

logp = np.log(daily['close'])

my_filter = MomentumFilter(np.log(daily['close']))
my_fit = my_filter.fit(method='lbfgs', bounds = ((0, 1), (0, 1)))
my_fit.summary()

plt.plot(logp[1:])
plt.plot(my_fit.fittedvalues)

# This should just be the logprice
plt.plot(my_fit.filtered_state[0, :])
plt.show()

# This is the drift term
plt.plot(my_fit.filtered_state[1, :])
