import xarray as xr
import numpy as np
import pandas as pd

class NetCDFReader:
    """Class to handle NetCDF timeseries data reading and preprocessing."""
    
    def __init__(self, file_path):
        """
        Initialize with path to NetCDF file.
        
        Parameters
        ----------
        file_path : str
            Path to the NetCDF file
        """
        self.file_path = file_path
        self.dataset = None
        
    def read_data(self, variable_name=None):
        """
        Read specified variable from NetCDF file.
        
        Parameters
        ----------
        variable_name : str, optional
            Name of the variable to read. If None, returns all variables
            
        Returns
        -------
        xarray.DataArray or xarray.Dataset
            The requested data
        """
        try:
            self.dataset = xr.open_dataset(self.file_path)
            if variable_name:
                if variable_name not in self.dataset:
                    raise ValueError(f"Variable {variable_name} not found in dataset. "
                                  f"Available variables: {list(self.dataset.data_vars)}")
                return self.dataset[variable_name]
            return self.dataset
        except Exception as e:
            raise ValueError(f"Error reading NetCDF file: {str(e)}")
    
    def get_timeseries(self, variable_name):
        """
        Extract timeseries for a specific variable.
        
        Parameters
        ----------
        variable_name : str
            Name of the variable to extract
            
        Returns
        -------
        xarray.DataArray
            Timeseries data for the specified variable
        """
        data = self.read_data(variable_name)
        return data
    
    def list_variables(self):
        """
        List all available variables in the dataset.
        
        Returns
        -------
        list
            List of variable names
        """
        if self.dataset is None:
            self.read_data()
        return list(self.dataset.data_vars)
    
    def get_date_range(self):
        """
        Get the start and end dates of the dataset.
        
        Returns
        -------
        tuple
            (start_date, end_date) as datetime objects
        """
        if self.dataset is None:
            self.read_data()
        dates = self.dataset.Date.values
        return pd.Timestamp(dates[0]), pd.Timestamp(dates[-1])
    
    def get_variable_statistics(self, variable_name):
        """
        Get basic statistics for a variable.
        
        Parameters
        ----------
        variable_name : str
            Name of the variable
            
        Returns
        -------
        dict
            Dictionary containing basic statistics
        """
        data = self.get_timeseries(variable_name)
        return {
            'mean': float(data.mean()),
            'std': float(data.std()),
            'min': float(data.min()),
            'max': float(data.max()),
            'missing_values': int(data.isnull().sum())
        }