import numpy as np

import panama.responses as responses
from panama.anita4 import ANITA4


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
            assert np.sum(trigger.time) > 1e-6
            assert np.sum(np.abs(trigger)) > 0.0

            # load the digitizer responses
            digitizer = responses.get_digitizer_response(channel, config, anita.flight)

            # and perform some basic tests
            assert np.sum(digitizer.time) > 1e-6
            assert np.sum(np.abs(digitizer)) > 0.0

            # and try and load the corresponding responses directly
            for response in ["trigger", "digitizer"]:
                _ = responses.get_response(response, channel, config, anita.flight)

    # and check that I also load the digitizer and
    # trigger responses directly from the instance
    trigger = anita.trigger_responses

    # and check that all the channels are present
    assert np.all(trigger.channels == anita.channels)
    assert np.all(trigger.configs == anita.configs)

    # and repeat for the digitizer response
    digitizer = anita.digitizer_responses

    # and check that all the channels are present
    assert np.all(digitizer.channels == anita.channels)
    assert np.all(digitizer.configs == anita.configs)
