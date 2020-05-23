"""
Load the S21 simulation of the ANITA-4 TUFFs.
"""
import os.path as op

import numpy as np
import xarray as xr

__all__ = ["get_response"]

# the list of simulated TUFF configs
configs = [
    "260_0_0",
    "260_375_0",
    "260_385_0",
    "260_365_0",
    "260_0_460",
    "260_375_460",
]


def is_config(config: str) -> bool:
    """
    Check that `config` is a valid ANITA4 TUFF config.

    Parameters
    ----------
    config: str
        A TUFF config string of the form X_X_X where X
        are frequencies in MHz.

    Returns
    -------
    valid: bool
        True if this is a valid TUFF configuration.
    """
    return config in configs


def get_response(config: str) -> xr.DataArray:
    """
    Return the simulated S21 magnitude response of an ANITA4 TUFF.

    This uses the averaged simulated TUFF response produced by
    O. Banerjee in ANITA E-Log 711.

    Parameters
    ----------
    config: str
        A valid TUFF configuration string.

    Returns
    -------
    response: xr.DataArray
        A DataArray indexed by 'freqs' in MHz.

    Raises
    ------
    ValueError
        If `config` is an invalid TUFF configuration.
    """

    # check if this is not a valid configuration
    if not is_config(config):
        raise ValueError(f"{config} is not a valid TUFF configuration.")

    # if we are here we have a valid TUFF configuration

    # get the directory where we store the TUFF files
    data_directory = op.abspath(
        op.join(
            __file__,
            op.pardir,
            op.pardir,
            op.pardir,
            "data",
            "calibration",
            "anita4",
            "tuff",
        )
    )

    # load the file
    data = np.loadtxt(op.join(data_directory, config + ".dat"))

    # create the data array
    response = xr.DataArray(data[:, 1], coords={"freqs": data[:, 0]}, dims="freqs")

    # label the independent variables
    response.freqs.attrs["units"] = "MHz"
    response.freqs.attrs["long_name"] = "Frequency"

    # and the dependent variable
    response.attrs["units"] = "dB"
    response.attrs["long_name"] = "S21"

    # and a description for this config
    response.attrs["config"] = config

    # and we are done
    return response
