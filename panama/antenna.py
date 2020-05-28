from os.path import dirname, join

import numpy as np
import xarray as xr

# the directory where we store impulse responses and antenna beamwidths
RESPONSE_DIR = join(dirname(dirname(__file__)), *("data", "responses"))


def get_beamwidth(flight: int) -> xr.Dataset:
    """
    Load the beam-width (HWHM) of the Seavey's for a given ANITA flight.

    Parameters
    ----------
    flight: int
        The ANITA flight to load.

    Returns
    -------
    response: xr.Dataset
        A DataArray containing 'freqs' in MHz, 'H' in degrees, and 'V' in degrees.

    Raises
    ------
    ValueError:
        If `flight` is not a valid ANITA flight.

    """

    # check that we only load valid flights
    if flight != 3 and flight != 4:
        raise ValueError(
            f"We currently only support loading the ANITA-{3,4} antenna gain."
        )

    # construct the filename given the current flight
    filename: str = join(RESPONSE_DIR, *(f"anita{flight}", "seavey_beamwidth.dat"))

    # load the data into a NumPy array
    data: np.ndarray = np.loadtxt(
        filename, dtype=[("freqs", float), ("H", float), ("V", float)],
    )

    # and create a dataset for the the horizontal plane
    H = xr.DataArray(data["H"], coords={"freqs": data["freqs"]}, dims="freqs")
    H.attrs["units"] = "deg"
    H.attrs["long_name"] = "Horizontal HWHM"

    # and create a dataset for the the vertical plane
    V = xr.DataArray(data["V"], coords={"freqs": data["freqs"]}, dims="freqs")
    V.attrs["units"] = "deg"
    V.attrs["long_name"] = "Vertical HWHM"

    # and create the dataset
    beamwidths = xr.Dataset({"H": H, "V": V})

    # label the independent variables
    beamwidths.freqs.attrs["units"] = "MHz"
    beamwidths.freqs.attrs["long_name"] = "Frequency"

    # and return the loaded beamwidths
    return beamwidths
