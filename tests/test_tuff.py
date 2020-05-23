"""
Test that I can load the TUFF configurations for the ANITA4 flight.
"""
import matplotlib.pyplot as plt
import numpy as np
import pytest

import panama.anita4.tuff as tuff
import panama.calibration.tuff as tuffcalib
from panama.anita4 import ANITA4

from . import figdir


def test_load_configs() -> None:
    """
    Load random configs and make sure they
    are all valid ANITA4 configs.
    """

    # construct the payload
    anita = ANITA4()

    for i in range(30):

        # choose a random time in the flight
        time = np.random.uniform(1480713196, 1482987943)

        # get the config at this time
        config = tuff.config(time)

        # and check that this is a valid config
        assert config in anita.configs


def test_invalid_configs() -> None:
    """
    Check that ValueError is thrown for times before
    and after the ANITA flight.
    """

    # before the flight
    with pytest.raises(ValueError):
        tuff.config(1480613000)

    # after the flight
    with pytest.raises(ValueError):
        tuff.config(1600000000)


def test_tuff_response() -> None:
    """
    Check that we can load and plot the average AMPA response.
    """

    # get the list of simulated TUFF configurations
    configs = tuffcalib.configs

    # create a figure and axis
    fig, ax = plt.subplots()

    # loop over the configs
    for config in configs:

        # get the response of this config
        response = tuffcalib.get_response(config)

        # plot the response
        ax.plot(response["freqs"], response, lw=0.8)

    # and add some info
    ax.set_xlim([100, 1300])
    ax.set_xlabel("Frequency [MHz]")
    ax.set_ylabel("S21 [dB]")
    ax.set_title("Simulated TUFF Responses")

    # and save the figure
    plt.savefig(f"{figdir}/anita4_tuff_responses.png")
