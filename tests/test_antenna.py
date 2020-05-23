"""
Test that we can load and plot ANITA antenna gains
"""
import matplotlib.pyplot as plt
import numpy as np

import panama.calibration.antenna as antenna

from . import figdir


def test_anita1_antenna() -> None:
    """
    Check that we can load and plot the average AMPA response.
    """

    # get the average response
    response = antenna.get_response(flight=1)

    # check that it matches the specific flight call
    np.testing.assert_allclose(response["H"], antenna.get_anita1_response()["H"])
    np.testing.assert_allclose(response["V"], antenna.get_anita1_response()["V"])

    # create a figure and axis
    fig, ax = plt.subplots()

    # plot the response
    ax.plot(response["freqs"], response["H"], label="H-Pol")
    ax.plot(response["freqs"], response["V"], label="V-Pol")

    # and some limits
    ax.set_ylim([0, 15])

    # and add some info
    ax.set_xlabel("Frequency [MHz]")
    ax.set_ylabel("Gain [dBi]")
    ax.set_title("Average ANITA-1 Antenna Gain")

    plt.savefig(f"{figdir}/anita1_antenna_gain.png")
