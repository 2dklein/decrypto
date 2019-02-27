# Hit or miss
# Monte Carlo Integration Method

import numpy as np
import random as rn
N = 1000000
xr = np.random.uniform(1,2,N)
yr = np.random.uniform(0,15,N)
count = 0.
area = 1*15.

for i in range(N):
    if yr[i] <= xr[i]**4. - 2.*xr[i] + 1.:
        count += 1.

integ = count*area/N

print integ