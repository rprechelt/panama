"""
Test that I can load the TUFF configurations for the ANITA4 flight.
"""
import numpy as np
import pytest

import panama.anita4.tuff as tuff
from panama.anita4 import ANITA4


def test_load_configs():
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


def test_invalid_configs():
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
