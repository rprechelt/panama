"""
Load gain and NF measurement of the ANITA-4 AMPA's.
"""
import os.path as op

import numpy as np
import xarray as xr

__all__ = ["get_response", "get_average_response"]


def get_response(channel: str = "average") -> xr.Dataset:
    """
    Load the measured S21 and NF of ANITA4 AMPA's.

    If `channel`=="average", try and load the average AMPA response.
    Otherwise, load the AMPA corresponding to a given ANITA4 channel.

    This was measured in ANITA E-Log 681.

    Parameters
    ----------
    channel: str
        The channel of the AMPA to load.

    Returns
    -------
    response: xr.Dataset
        A DataArray containing 'freqs' in MHz, 'gain' in dB, and 'noise' in K.

    Raises
    ------
    ValueError:
        If `channel` is not found in the data directory.

    """

    # if we want the average response
    if channel == "average":
        return get_average_response()
    else:
        raise ValueError(
            f"We currently only support loading the average AMPA response."
        )


def get_average_response() -> xr.Dataset:
    """
    Load the average measured S21 and NF of the ANITA4 AMPA's.

    This was measured in ANITA e-Log 681.

    Parameters
    ----------

    Returns
    -------
    response: xr.Dataset
        A DataArray containing 'freqs' in MHz, 'gain' in dB, and 'noise' in K.

    """

    # if we are here we have a valid TUFF configuration

    # get the directory where we store the TUFF files
    data_directory = op.abspath(
        op.join(
            __file__, op.pardir, op.pardir, op.pardir, "data", "calibration", "anita4"
        )
    )

    # load the file
    data = np.loadtxt(op.join(data_directory, "average_ampa.dat"))

    # create the S21 array with some units
    S21 = xr.DataArray(data[:, 1], coords={"freqs": data[:, 0]}, dims="freqs")
    S21.attrs["units"] = "dB"
    S21.attrs["long_name"] = "S21"

    # and the noise figure array
    NF = xr.DataArray(data[:, 2], coords={"freqs": data[:, 0]}, dims="freqs")
    NF.attrs["units"] = "K"
    NF.attrs["long_name"] = "NF"

    # and create the dataset
    response = xr.Dataset({"S21": S21, "NF": NF})

    # label the independent variables
    response.freqs.attrs["units"] = "MHz"
    response.freqs.attrs["long_name"] = "Frequency"

    # and we are done
    return response
