"""
Load the gains of various ANITA horn antennas.
"""
import os.path as op

import numpy as np
import xarray as xr

__all__ = [
    "get_response",
    "get_anita1_response",
    "get_anita3_response",
    "get_anita3_datasheet_response",
]


def get_response(flight: int) -> xr.Dataset:
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
    if flight == 1 or flight == 2:
        return get_anita1_response()
    elif flight == 3 or flight == 4:
        return get_anita3_response()
    else:
        raise ValueError(
            f"We currently only support loading the ANITA-{1,2,3,4} antenna gain."
        )


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
    response = xr.Dataset({"H": HH, "HV": HV, "V": VV, "VH": VH})

    # label the independent variables
    response.freqs.attrs["units"] = "MHz"
    response.freqs.attrs["long_name"] = "Frequency"

    # and we are done
    return response


def get_anita3_response() -> xr.Dataset:
    """
    Load the measured antenna gain for an ANITA-3 horn.

    *WARNING*: Use these with care. These measurements disagree by
    nearly a factor of 2 with the Seavey datasheet.

    This was measured by B. Rotter and B. Strutt in Palestine
    and is discussed in Elog 575.
    https://elog.phys.hawaii.edu/elog/anita_notes/575

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
            __file__, op.pardir, op.pardir, op.pardir, "data", "calibration", "anita3"
        )
    )

    # load the file
    Hgain = np.loadtxt(op.join(data_directory, "hpol_seavey_gain.dat"))
    Vgain = np.loadtxt(op.join(data_directory, "vpol_seavey_gain.dat"))

    # HPol -> HPol
    HH = xr.DataArray(Hgain[:, 1], coords={"freqs": Hgain[:, 0]}, dims="freqs")
    HH.attrs["units"] = "dBi"
    HH.attrs["long_name"] = r"HPol $\rightarrow$ HPol"

    # VPol -> VPol
    VV = xr.DataArray(Vgain[:, 1], coords={"freqs": Vgain[:, 0]}, dims="freqs")
    VV.attrs["units"] = "dBi"
    VV.attrs["long_name"] = r"VPol $\rightarrow$ VPol"

    # and create the dataset
    response = xr.Dataset({"H": HH, "V": VV})

    # label the independent variables
    response.freqs.attrs["units"] = "MHz"
    response.freqs.attrs["long_name"] = "Frequency"

    # and we are done
    return response


def get_anita3_datasheet_response() -> xr.Dataset:
    """
    Load the Seavey datasheet antenna gain for an ANITA-3/4 horn

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
            __file__, op.pardir, op.pardir, op.pardir, "data", "calibration", "anita3"
        )
    )

    # load the file
    gain = np.loadtxt(op.join(data_directory, "seavey_datasheet_gain.dat"))

    # HPol -> HPol
    HH = xr.DataArray(gain[:, 1], coords={"freqs": gain[:, 0]}, dims="freqs")
    HH.attrs["units"] = "dBi"
    HH.attrs["name"] = r"H"
    HH.attrs["long_name"] = r"HPol $\rightarrow$ HPol"

    # VPol -> VPol
    VV = xr.DataArray(gain[:, 2], coords={"freqs": gain[:, 0]}, dims="freqs")
    VV.attrs["units"] = "dBi"
    HH.attrs["name"] = r"V"
    VV.attrs["long_name"] = r"VPol $\rightarrow$ VPol"

    # and create the dataset
    response = xr.Dataset({"H": HH, "V": VV})

    # label the independent variables
    response.freqs.attrs["units"] = "MHz"
    response.freqs.attrs["long_name"] = "Frequency"

    # and we are done
    return response
