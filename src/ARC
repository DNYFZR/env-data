# Asset Replacement Class
import pandas as pd
from functools import cache
from numpy import random, mean, array, append, divide

# random seed for repeatability 
random.seed(8)

'''
NOTES:
- Code writted in Python 3.9.10 + NumPy 1.22.3 + Pandas 1.4.2
'''
class AssetReplacementClass:
    '''
        This class calculated the survival probability for a normal distribution over a user defined numbre of years. 
    '''

    def __init__(self, df, n_years, n_samples):
        self.df = df
        self.years = [i for i in range(n_years)]
        self.samples = n_samples

        self.base = array([])
        self.cond = array([])


        self.ages = df['Years'].to_numpy()
        self.means = df['mean life'].to_numpy()
        self.devs = df['stdev life'].to_numpy()
        self.iters = range(len(self.ages))

    @staticmethod
    @cache
    def survival_probability(age_model, age_mean, age_stdev, n_samples):    
        '''
            Takes input data and calculates a survivial probability curve using a normal distribution
            around a mean and standard deviation.
        '''

        p_dist = array(random.normal(age_mean, age_stdev, n_samples))
        return mean([1 if j - age_model >= 0 else 0 for j in p_dist])
  
 
    def base_probability(self):
        '''
            Uses survival_probabilities function to generate the survival probability of the asset at it's current age.
        '''
        self.base = array([self.survival_probability(self.ages[i], self.means[i], self.devs[i], self.samples) for i in self.iters])


    def conditional_probability(self):
        '''
            Calculates the conditional probability for a given future age.
        '''
        # Probability for current age
        p_a = array([self.survival_probability(self.ages[i] + self.years[0], self.means[i], self.devs[i], self.samples) for i in self.iters])

        # Probability of survival (base)
        p_b = self.base
        
        # Probability of b given a 
        if self.years[0] == 0:
            p_ba = self.base
        else: 
            p_ba = array([self.survival_probability(self.ages[i] + self.years[0] - 1, self.means[i], self.devs[i], self.samples) for i in self.iters])

        # calculate conditional probability
        for i in self.iters:
            if p_b[i] == 0:
                result = 0
            else:
                result = divide(p_a[i] * p_ba[i], p_b[i])        
            self.cond = append(self.cond, result)

    def run_ARC(self):
        # calculate base probabilities
        self.base_probability()
        self.df['year_0'] = self.base

        # Calcualte over self.years time frame
        for i in range(len(self.years)):
            self.conditional_probability()
            
            self.df[f'year_{i + 1}'] = self.cond

            self.years.pop(0)
            self.cond = array([])
            self.df = self.df.copy()
        return self.df


if __name__ == '__main__':
    from time import time
    
    # if taking a cut of the df - remember to reset_index(drop = True)
    df = pd.read_csv('test_100k.csv')
    print(f'Rows : {df.shape[0]}')
    
    # Time run
    start = time()
    df_out = AssetReplacementClass(df.copy(), n_years=50, n_samples=1_000).run_ARC()

    print(f'Run complete : {round((time() - start) / 60, 1)} min')
    
    # Save test data
    df_out.to_csv('ARC_test.csv', chunksize=5000)
    
