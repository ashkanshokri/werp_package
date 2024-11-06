import numpy as np

class ResilienceMetrics:
    """Class to calculate resilience and reliability metrics."""
    
    def __init__(self, timeseries, threshold):
        """Initialize with timeseries data and threshold."""
        self.timeseries = timeseries
        self.threshold = threshold
        
    def calculate_reliability(self):
        """
        Calculate reliability as the percentage of time the system is above threshold.
        """
        total_points = len(self.timeseries)
        points_above_threshold = np.sum(self.timeseries >= self.threshold)
        reliability = (points_above_threshold / total_points) * 100
        return reliability
    
    def calculate_resilience(self):
        """
        Calculate resilience as the average recovery rate after falling below threshold.
        """
        failures = self.timeseries < self.threshold
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
            
        return 100.0 / (1 + np.mean(recovery_times))  # Normalize to 0-100 scale 