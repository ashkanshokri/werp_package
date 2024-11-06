import numpy as np
import xarray as xr
import pandas as pd
from datetime import datetime
from pathlib import Path

def create_sample_dataset(
    start_date='1889-01-01',
    end_date='2018-12-31',
    base_value=0.8,
    seasonal_amplitude=0.2,
    noise_level=0.1
):
    """
    Create a sample NetCDF dataset with synthetic EFR timeseries data.
    
    Parameters
    ----------
    start_date : str
        Start date for the timeseries (default: '1889-01-01')
    end_date : str
        End date for the timeseries (default: '2018-12-31')
    base_value : float
        Mean value for the variables (default: 0.8)
    seasonal_amplitude : float
        Amplitude of seasonal variation (default: 0.2)
    noise_level : float
        Standard deviation of random noise (default: 0.1)
    
    Returns
    -------
    xarray.Dataset
        Sample dataset with synthetic timeseries
    """
    # Create date range
    dates = pd.date_range(start=start_date, end=end_date, freq='D')
    
    # Create the basic data arrays
    n_days = len(dates)
    
    # Define EFR variables to create
    efr_vars = [
        'MACQ_CC_EFR01.aal', 'MACQ_CC_EFR01.eal', 
        'MACQ_CC_EFR01.hal', 'MACQ_CC_EFR01.ehl',
        'MACQ_CC_EFR02.aal', 'MACQ_CC_EFR02.eal', 
        'MACQ_CC_EFR02.hal', 'MACQ_CC_EFR02.ehl'
    ]
    
    data_vars = {}
    
    for var in efr_vars:
        # Create synthetic data for each variable
        # Add seasonal variation
        t = np.arange(n_days)
        seasonal = seasonal_amplitude * np.sin(2 * np.pi * t / 365.25)
        
        # Add trend and noise
        if '.aal' in var:
            # Annual average low flow - slight upward trend
            trend = 0.0001 * t
        elif '.eal' in var:
            # Extreme annual low flow - slight downward trend
            trend = -0.0001 * t
        elif '.hal' in var:
            # High annual low flow - stable
            trend = 0
        else:  # .ehl
            # Extreme high low flow - more variable
            trend = 0.00005 * np.sin(2 * np.pi * t / (365.25 * 10))
        
        # Combine components and add noise
        data = (base_value + trend + seasonal + 
                np.random.normal(0, noise_level, n_days))
        
        # Ensure values are positive and reasonable
        data = np.clip(data, 0, 2) * 100
        
        # Add to dataset
        data_vars[var] = (('Date'), data.astype(np.float32))
    
    # Create xarray dataset
    ds = xr.Dataset(
        data_vars=data_vars,
        coords={
            'Date': dates
        },
        attrs={
            'description': 'Sample EFR dataset for resilience metrics testing',
            'created': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
    )
    
    return ds

def save_sample_dataset(filename='data/sample_data.nc'):
    """
    Generate and save a sample dataset to a NetCDF file.
    
    Parameters
    ----------
    filename : str
        Name of the file to save the dataset
        
    Returns
    -------
    str
        Path to the saved file
    """
    # Create data directory if it doesn't exist
    data_dir = Path(filename).parent
    data_dir.mkdir(parents=True, exist_ok=True)     
       
    ds = create_sample_dataset()
    ds.to_netcdf(filename)
    print(f"Sample dataset saved to {filename}")
    return filename

if __name__ == '__main__':
    # Example usage
    filename = save_sample_dataset()