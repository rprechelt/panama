"""
Load the gains of various ANITA horn antennas.
"""
import os.path as op

import numpy as np
import xarray as xr

__all__ = ["get_response", "get_anita1_response"]


def get_response(flight: int = 1) -> xr.Dataset:
    """
    Load the measured gain of an ANITA horn antenna for a given flight.

    Parameters
    ----------
    flight: int
        The ANITA flight to load.

    Returns
    -------
    response: xr.Dataset
        A DataArray containing 'freqs' in MHz, 'H' in dBi, and 'V' in dBi.

    Raises
    ------
    ValueError:
        If `channel` is not found in the data directory.

    """

    # if we want the average response
    if flight == 1:
        return get_anita1_response()
    else:
        raise ValueError(f"We currently only support loading the ANITA-1 antenna gain.")


def get_anita1_response() -> xr.Dataset:
    """
    Load the measured antenna gain for an ANITA-1 horn.

    This was measured by Ped in ANITA E-Log 71:
    https://elog.phys.hawaii.edu/elog/anita_notes/71

    Parameters
    ----------

    Returns
    -------
    response: xr.Dataset
        A Dataset containing 'freqs' in MHz, 'H' in dBi, and 'V' in dBi.

    """

    # if we are here we have a valid TUFF configuration

    # get the directory where we store the TUFF files
    data_directory = op.abspath(
        op.join(
            __file__, op.pardir, op.pardir, op.pardir, "data", "calibration", "anita1"
        )
    )

    # load the file
    gains = np.loadtxt(op.join(data_directory, "seavey_gain.dat"))

    # HPol -> HPol
    HH = xr.DataArray(gains[:, 1], coords={"freqs": gains[:, 0]}, dims="freqs")
    HH.attrs["units"] = "dBi"
    HH.attrs["long_name"] = r"HPol $\rightarrow$ HPol"

    # HPol -> VPol
    HV = xr.DataArray(gains[:, 2], coords={"freqs": gains[:, 0]}, dims="freqs")
    HV.attrs["units"] = "dBi"
    HV.attrs["long_name"] = r"HPol $\rightarrow$ VPol"

    # VPol -> VPol
    VV = xr.DataArray(gains[:, 3], coords={"freqs": gains[:, 0]}, dims="freqs")
    VV.attrs["units"] = "dBi"
    VV.attrs["long_name"] = r"VPol $\rightarrow$ VPol"

    # VPol -> HPol
    VH = xr.DataArray(gains[:, 4], coords={"freqs": gains[:, 0]}, dims="freqs")
    VH.attrs["units"] = "dBi"
    VH.attrs["long_name"] = r"VPol $\rightarrow$ HPol"

    # and create the dataset
    response = xr.Dataset({"H": HH, "HX": HV, "V": VV, "VX": VH})

    # label the independent variables
    response.freqs.attrs["units"] = "MHz"
    response.freqs.attrs["long_name"] = "Frequency"

    # and we are done
    return response
