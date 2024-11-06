import xarray as xr
import numpy as np

class NetCDFReader:
    """Class to handle NetCDF timeseries data reading and preprocessing."""
    
    def __init__(self, file_path):
        """Initialize with path to NetCDF file."""
        self.file_path = file_path
        self.dataset = None
        
    def read_data(self, variable_name):
        """Read specified variable from NetCDF file."""
        try:
            self.dataset = xr.open_dataset(self.file_path)
            return self.dataset[variable_name]
        except Exception as e:
            raise ValueError(f"Error reading NetCDF file: {str(e)}")
    
    def get_timeseries(self, variable_name, lat=None, lon=None):
        """Extract timeseries for a specific location if lat/lon provided."""
        data = self.read_data(variable_name)
        if lat is not None and lon is not None:
            return data.sel(latitude=lat, longitude=lon, method='nearest')
        return data 