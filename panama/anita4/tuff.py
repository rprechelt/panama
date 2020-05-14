from os.path import dirname, join

import numpy as np

__all__ = ["config"]

# the directory where we store the responses
RESPONSE_DIR = join(dirname(dirname(dirname(__file__))), *("data", "responses"))

# load the TUFF config file
config_by_time = np.loadtxt(
    join(RESPONSE_DIR, *("anita4", "tuff_by_time.dat")),
    dtype=[("config", object), ("time", int)],
)


def config(time: int) -> str:
    """
    Get the string representing the TUFF configuration
    active at a given unix time.

    This returns the filter configuration separated by
    underscores i.e. 260_375_0. A '0' indicates that
    the notche was not enabled.

    Parameters
    ----------
    time: int
        The unix time of the event in question.

    Returns
    -------
    config: str
        The string identifying the TUFF config
    """

    # check that the time is valid for the A4 flight.
    if time < config_by_time["time"][0]:
        raise ValueError(f"{time} is before the A4 flight.")
    elif time > config_by_time["time"][-1]:
        raise ValueError(f"{time} is after the A4 flight.")

    # find the last config before the time as that is when it changed
    index = np.where(config_by_time["time"] < time)[0][-1]

    # get the configuration
    active_config: str = config_by_time["config"][index]

    # and return the appropriate config
    return active_config
