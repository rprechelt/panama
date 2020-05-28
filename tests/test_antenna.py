"""
Test that we can load and plot ANITA antenna gains
"""
import matplotlib.pyplot as plt
import numpy as np

import panama.antenna as antenna
import panama.calibration.antenna as calantenna

from . import figdir

def test_anita34_beamwidths() -> None:
    """
    Check that we can load and plot the ANITA-3/4 antenna beamwidths.
    """

    # loop over the flights
    for flight in [3, 4]:

        # create a figure and axis
        fig, ax = plt.subplots()

        # load the beamwidths
        beamwidths = antenna.get_beamwidth(flight)

        # check that frequencies are in the right range
        np.testing.assert_array_less(beamwidths.freqs, 1300.)
        np.testing.assert_array_less(50., beamwidths.freqs)

        # and plot the H and V planes
        ax.plot(beamwidths.freqs, beamwidths.H, label="Horiz.")
        ax.plot(beamwidths.freqs, beamwidths.V, label="Vertical.")

        # and some titles and labels
        ax.set_title(f"ANITA-{flight} Seavey Beamwidths")
        ax.set_xlabel("Frequency [MHz]")
        ax.set_ylabel("Half-Width Half-Max (HWHM) [deg]")

        # and save the figure
        plt.savefig(f"{figdir}/anita{flight}_seavey_beamwidths.png")


def test_anita1_antenna() -> None:
    """
    Check that we can load and plot the average AMPA response.
    """

    # get the average response
    response = calantenna.get_response(flight=1)

    # check that it matches the specific flight call
    np.testing.assert_allclose(response["H"], calantenna.get_anita1_response()["H"])
    np.testing.assert_allclose(response["V"], calantenna.get_anita1_response()["V"])

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
