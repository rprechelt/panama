import numpy as np
from panama.anita4 import ANITA4
import panama.responses as responses


def test_get_responses_anita4() -> None:
    """
    Check that we can explicitly load the trigger and digitizer responses for
    ANITA4 every channel using the explicit and general-purpose methods.
    """

    # create a reference to ANITA4
    anita = ANITA4()

    # loop over every channel in ANITA
    for channel in anita.channels:

        # and every TUFF config and averages
        for config in anita.configs:

            # load the trigger responses
            trigger = responses.get_trigger_response(channel, config, anita.flight)

            # and perform some basic tests
            assert np.sum(trigger["time"]) > 1e-6
            assert np.sum(np.abs(trigger["height"])) > 0.0

            # load the digitizer responses
            digitizer = responses.get_digitizer_response(channel, config, anita.flight)

            # and perform some basic tests
            assert np.sum(digitizer["time"]) > 1e-6
            assert np.sum(np.abs(digitizer["height"])) > 0.0

            # and try and load the corresponding responses directly
            for response in ["trigger", "digitizer"]:
                _ = responses.get_response(response, channel, config, anita.flight)
