"""
Test that we can load and plot AMPA responses.
"""
import matplotlib.pyplot as plt

import panama.calibration.ampa as ampa

from . import figdir


def test_average_ampa():
    """
    Check that we can load and plot the average AMPA response.
    """

    # get the average response
    average = ampa.get_average_response()

    # create a figure and axis
    fig, ax = plt.subplots()

    # plot the response
    ax.plot(average["freqs"], average["S21"], c="k")

    # create a twin-y axis to plot the noise figure
    ax2 = ax.twinx()
    ax2.plot(average["freqs"], average["NF"], c="r")

    # and add some info
    ax.set_xlabel("Frequency [MHz]")
    ax.set_ylabel("S21 [dB]")
    ax2.set_ylabel("Noise Figure [K]")
    ax.set_title("Average ANITA-4 AMPA Response")

    plt.savefig(f"{figdir}/anita4_average_ampa.png")
