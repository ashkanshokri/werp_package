import numpy as np
import xarray as xr


if __name__ == '__main__':
    ds1 = xr.open_dataset('P:/work/sho108/werp/results/cc_results/r0.9_e1.06/1170/allocations.nc')
    ds2 = xr.open_dataset('P:/work/sho108/werp/results/cc_results/r0.7_e1.0/0/allocations.nc')
    ds3 = xr.open_dataset('P:/work/sho108/werp/results/cc_results/r0.7_e1.0/2730/allocations.nc')


    ds_dict = {'r0.9_e1.06': ds1, 'r0.7_e1.0': ds2}

    # Get the years from both datasets
    years = [ds.Date.dt.year.values for ds in ds_dict.values()]

    # Create a combined list of years
    all_years = np.unique(np.concatenate(years))

    # Randomly select years from the combined list
    selected_years = np.random.choice(all_years, size=len(all_years), replace=False)

    # Create an empty dataset to hold the mixed data
    mixed_data = {}

    # Loop through the selected years and mix data from ds1 and ds2
    for year in selected_years:
        chosen_ds_key = np.random.choice(list(ds_dict.keys()))
        chosen_ds = ds_dict[chosen_ds_key]
        # Select data for the chosen year and add to mixed_data
        mixed_data[year] = chosen_ds.sel(Date=chosen_ds.Date.dt.year == year)

    # Combine the mixed data into a new dataset
    mixed_ds = xr.concat(list(mixed_data.values()), dim='Date').sortby('Date')
    mixed_ds.to_netcdf('data/sample_data.nc')


