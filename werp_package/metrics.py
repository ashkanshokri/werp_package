import numpy as np
import pandas as pd

class ResilienceMetrics:
    """Class to calculate resilience and reliability metrics."""
    
    def __init__(self, timeseries, threshold, cutoff_date='06-30'):
        """Initialize with timeseries data, threshold, and cutoff date."""
        self.timeseries = timeseries
        self.threshold = threshold
        self.cutoff_date = pd.to_datetime(cutoff_date, format='%m-%d')
        
    def filter_timeseries_at_cutoff(self):
        """Filter timeseries to only include values at the cutoff date each year."""
        # Assuming timeseries is a pandas DataFrame with a DateTime index
        return self.timeseries[np.logical_and(self.timeseries.Date.dt.month == self.cutoff_date.month, self.timeseries.Date.dt.day == self.cutoff_date.day)]
    
    def calculate_reliability(self):
        """
        Calculate reliability as the percentage of time the system is above threshold.
        """
        filtered_timeseries = self.filter_timeseries_at_cutoff()
        total_points = len(filtered_timeseries)
        points_above_threshold = np.sum(filtered_timeseries >= self.threshold)
        reliability = (points_above_threshold / total_points) * 100 if total_points > 0 else 0
        return reliability
    
    def calculate_resilience(self):
        """
        Calculate resilience as the average recovery rate after falling below threshold.
        """
        filtered_timeseries = self.filter_timeseries_at_cutoff()
        failures = filtered_timeseries < self.threshold
        recovery_times = []
        failure_duration = 0
        
        for i in range(1, len(failures)):
            if failures[i]:
                failure_duration += 1
            elif failure_duration > 0:
                recovery_times.append(failure_duration)
                failure_duration = 0
                
        if len(recovery_times) == 0:
            return 100.0  # Perfect resilience if no failures
            
        return 100.0 / (np.mean(recovery_times))  # Normalize to 0-100 scale 
    

class DeliberyToOrderRatio:
    """Class to calculate high security metrics."""
    
    def __init__(self, timeseries):
        """Initialize with timeseries data."""
        self.timeseries = timeseries
    
    def yearly_cumsum(self, df):
        b = pd.concat([df.loc[f'{y}'].cumsum() for y in df.index.year.unique()])
        return b.sort_index()
    
    def cal_del_to_order_ratio(self, timestep='ME'):
        df_cumsum = self.yearly_cumsum(self.timeseries)
        ratio = df_cumsum['On Alloc div.'] / df_cumsum['Orders']

        if timestep:
            return ratio.resample(timestep).last()
        else:
            return ratio
        