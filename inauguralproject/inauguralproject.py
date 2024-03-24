import numpy as np
import pandas as pd
import scipy 
from types import SimpleNamespace
from scipy.optimize import root
import matplotlib.pyplot as plt

class ExchangeEconomyClass:

    def __init__(self):

        par = self.par = SimpleNamespace()

        # a. preferences
        par.alpha = 1/3
        par.beta = 2/3

        # b. endowments
        par.w1A = 0.8
        par.w2A = 0.3
        par.w1B = 1-0.8
        par.w2B = 1-0.3

        # c. Numeraire
        par.p2=1

    def utility_A(self,x1A,x2A):
        par = self.par
        uA = x1A**(par.alpha)*x2A**(1-par.alpha)
        return uA

    def utility_B(self,x1B,x2B):
        par = self.par
        uB= x1B**(par.beta)*x2B**(1-par.beta)
        return uB

    def demand_A(self,p1):
        par = self.par
        dap1= par.alpha*((p1*par.w1A+1*par.w2A)/p1)
        dap2=(1-par.alpha)*((p1*par.w1A+1*par.w2A)/(1))
        return dap1, dap2

    def demand_B(self,p1):
        par = self.par
        dbp1=par.beta*((p1*par.w1B+1*par.w2B)/p1)
        dbp2= (1-par.beta)*((p1*par.w1B+1*par.w2B)/par.p2)
        return dbp1, dbp2

    #Q2#

    def check_market_clearing(self,p1):

        par = self.par

        x1A,x2A = self.demand_A(p1)
        x1B,x2B = self.demand_B(p1)

        eps1 = x1A-par.w1A + x1B-(1-par.w1A)
        eps2 = x2A-par.w2A + x2B-(1-par.w2A)

        return eps1,eps2

    
    def added_errors(eps1,eps2):
        par = self.par
        eps=eps1+eps2
        return eps


    def market_clearing_error(self, p1):
        eps1, eps2 = self.check_market_clearing(p1)
        return eps1 + eps2
        
    def find_market_clearing_price(self, p1_guess):
        result = root(self.market_clearing_error, p1_guess)
        if result.success:
            return result.x[0]



    #Q4a#

    def find_best_allocation_0(self):
        par = self.par

        # set of prices
        p1_2=[0.5]
        for n in range(1, 76):
            p1_2.append(0.5+2*n/75)

        max_utility = -np.inf
        best_allocation = None
        best_price = None

        for p1 in p1_2:
            # Compute demands
            x1B, x2B = self.demand_B(p1)
            x1A = 1 - x1B
            x2A = 1 - x2B

            # Compute utility for A
            uA_0 = self.utility_A(x1A, x2A)

            # Update maximum utility and best allocation
            if abs(uA_0) > max_utility:
                max_utility = abs(uA_0)
                best_allocation_0 = (x1A, x2A, x1B, x2B)
                best_price_0 = p1

        return best_allocation_0, best_price_0


    #Q4.b:#

    def utility_A_negative(self,p1):
        par = self.par
        new_x1 = 1 - (par.beta * (p1* (1-par.w1A) + 1- par.w2A)/p1)
        new_x2 = 1 - ((1-par.beta) *(p1* (1-par.w1A) + (1-par.w2A)))
        negative_utility = -(new_x1**(par.alpha)*new_x2**(1-par.alpha))
        return negative_utility



    #Q5.a:#


    #Q5.b#

    def utility_A_negative_2(self, x): 
        par = self.par
        x1A = x[0]
        x2A = x[1]
        return -(x1A**(par.alpha)*x2A**(1-par.alpha))


    #Q6.a#

    def aggregate_utility(self,x):
        par=self.par
        x1A = x[0]
        x2A = x[1]
        A_U= self.utility_A(x1A,x2A)+self.utility_B(1-x1A,1-x2A)
        return -A_U



    #Q8#
            
    def market_clearing_price_8(self):
        result_8 = scipy.optimize.minimize_scalar(self.market_clearing_error, bounds=(0.01,10), method='bounded')
        if result_8.success:
            return result_8.x





