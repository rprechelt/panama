from os.path import dirname, join
from typing import Dict, List

import numpy as np
from cachetools import cached

__all__ = ["get_response", "get_trigger_response", "get_digitizer_response"]


# the directory where we store impulse responses
RESPONSE_DIR = join(dirname(dirname(__file__)), *("data", "responses"))


def get_all_responses(
    response: str, channels: List[str], configs: List[str], flight: int
) -> Dict[str, np.ndarray]:
    """
    """

    # a dictionary to store our responses
    responses: Dict[str, Dict[str, np.ndarray]] = {}

    # loop through all the channels and configs
    for ch in channels:
        responses[ch] = {}  # create a config dictionary
        for config in configs:
            responses[ch][config] = get_response(response, ch, config, flight)

    # and return the responses
    return responses


@cached(cache={})
def get_response(response: str, channel: str, config: str, flight: int) -> np.ndarray:
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
    impulse: np.ndarray
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
    # we load these into a NumPy Structured array and return
    responses: np.ndarray = np.loadtxt(
        filename, delimiter=" ", dtype=[("time", float), ("height", float)],
    )

    return responses


def get_trigger_response(
    channel: str, config: str = "0_0_0", flight: int = 4,
) -> np.ndarray:
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
    impulse: np.ndarray
        The impulse response/effective height in m/s sampled at 10 GSa/s.
    """

    # get the responses - explicitly annotate the type.
    responses: np.ndarray = get_response("digitizer", channel, config, flight)

    # and we are
    return responses


def get_digitizer_response(
    channel: str, config: str = "0_0_0", flight: int = 4,
) -> np.ndarray:
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
    responses: np.ndarray = get_response("digitizer", channel, config, flight)

    # and we are
    return responses
