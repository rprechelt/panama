from os.path import dirname, join
from typing import List

import numpy as np
import xarray as xr
from cachetools import cached

__all__ = ["get_response", "get_trigger_response", "get_digitizer_response"]


# the directory where we store impulse responses
RESPONSE_DIR = join(dirname(dirname(__file__)), *("data", "responses"))


def get_all_responses(
    response: str, channels: List[str], configs: List[str], flight: int
) -> xr.DataArray:
    """
    """

    # the number of channels that we load
    nchannels: int = len(channels)

    # the number of configs that loading
    nconfigs: int = len(configs)

    # get an reference response to get the length
    N: int = get_response(response, channels[0], configs[0], flight).size

    # allocate the memory for the response waveforms
    responses: np.ndarray = np.zeros((nchannels, nconfigs, N))

    # loop through all the channels
    for ich, ch in enumerate(channels):

        # and loop over the configs
        for iconfig, config in enumerate(configs):

            # get the current response
            waveform = get_response(response, ch, config, flight)

            # store the response in the array
            time = waveform.time  # type: ignore
            responses[ich, iconfig, :] = waveform  # type: ignore

    # and create the data array
    xray = xr.DataArray(
        responses,
        dims=["channels", "configs", "time"],
        coords={"channels": channels, "configs": configs, "time": time,},
    )

    # and return the responses
    return xray


@cached(cache={})
def get_response(response: str, channel: str, config: str, flight: int) -> xr.DataArray:
    """
    Load arbitrary impulse response from a directory organized according to the
    standard PANAMA response directories.

    This returns the time and amplitude of the impulse response as contained in
    the file - no error checking is currently performed. The rest of the PANAMA
    code base expects that impulse responses be sampled at 10 GSa/s (currently)
    with effective heights stored in m/s.

    This function loads directories of the form:

    ```
    data/{response}/anita{flight}/{response}/averages/{config}.imp
    data/{response}/anita{flight}/{response}/notches_{config}/{channel}.imp
    ```

    This is most commonly used with response="trigger" or response="digitizer"
    to load the trigger and digitizer impulse responses.


    Parameters
    ----------
    response: str
       The directory name of the type of response to load.
    channel: str
       The channel identifier for the channel to load or 'average'.
    config: str
       The TUFF configuration to load the response for.
    flight: int
       The ANITA flight to load the responses for.

    Returns
    -------
    impulse: xr.DataArray
        The impulse response/effective height in m/s sampled at 10 GSa/s.
    """
    # get the directory for this flight
    load_dir = join(RESPONSE_DIR, *(f"anita{flight}", response))

    # if the user asks for an average
    if channel == "average":
        filename = join(load_dir, *("averages", f"notches_{config}.imp"))
    else:
        filename = join(load_dir, *(f"notches_{config}", f"{channel}.imp"))

    # load the impulse response - these are stored calibrated and ready to use
    # we load these into a NumPy Structured array
    raw: np.ndarray = np.loadtxt(filename, delimiter=" ")

    # and convert it into an XArray DataArray
    return xr.DataArray(raw[:, 1], dims=["time"], coords={"time": raw[:, 0]},)


def get_trigger_response(
    channel: str, config: str = "0_0_0", flight: int = 4,
) -> xr.DataArray:
    """
    Load the trigger impulse response for a given channel,
    TUFF configuration, and ANITA flight.

    Parameters
    ----------
    channel: str
       The channel identifier for the channel to load or 'average'.
    config: str
       The TUFF configuration to load the response for.
    flight: int = 4
       The ANITA flight to load the responses for.

    Returns
    -------
    impulse: xr.DataArray
        The impulse response/effective height in m/s sampled at 10 GSa/s.
    """

    # get the responses - explicitly annotate the type.
    responses: np.ndarray = get_response("digitizer", channel, config, flight)

    # and we are
    return responses


def get_digitizer_response(
    channel: str, config: str = "0_0_0", flight: int = 4,
) -> xr.DataArray:
    """
    Load the digitizer impulse response for a given channel,
    TUFF configuration, and ANITA flight.

    Parameters
    ----------
    channel: str
       The channel identifier for the channel to load or 'average'.
    config: str
       The TUFF configuration to load the response for.
    flight: int = 4
       The ANITA flight to load the responses for.

    Returns
    -------
    impulse: np.ndarray
        The impulse response/effective height in m/s sampled at 10 GSa/s.
    """

    # get the responses - explicitly annotate the type.
    responses: xr.DataArray = get_response("digitizer", channel, config, flight)

    # and we are
    return responses
