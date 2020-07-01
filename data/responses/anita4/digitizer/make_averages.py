#!/usr/bin/env python3
import glob
import os
import os.path as op
from typing import List

import numpy as np

import align

# the configs that we process
configs = ["260_0_0", "260_0_460", "260_365_0", "260_375_0", "260_375_460", "260_385_0"]

# the current directory
curr_dir = op.dirname(op.abspath(__file__))

# the directory where we store the averages
avg_dir = op.join(curr_dir, "averages")

# make the output directory
os.makedirs(avg_dir, exist_ok=True)

# loop over all the configs
for config in configs:

    # and a quick status message
    print(f"Producing average for {config}")

    # and for each polarization
    for pol in ["H", "V", "?"]:

        # get the files associated with this config
        files = glob.glob(f"notches_{config}/???{pol}.imp")

        # a sanity check
        if len(files) == 0:
            raise RuntimeError(f"Unable to find files for {config}")

        # remove 13BH from the averages
        files = list(filter(lambda fname: "13BH" not in fname, files))

        # we define a lambda function to make an average
        def make_average(ref: np.ndarray, files: List[str]) -> np.ndarray:
            """
            Align the waveforms from `files` to `ref` the
            average waveform
            """

            # make a copy of the reference
            average = np.zeros_like(ref)

            # loop over the files
            for f in files:

                # load the waveform
                wvfm = np.loadtxt(f)

                # and align it with the reference
                aligned = align.align(ref, wvfm[:, 1], method="xcorr", factor=10)

                # and add it to the reference
                average += aligned

            # and return the average
            return average / float(len(files))

        # load the first waveform
        first = np.loadtxt(files[0])

        # we first create an average using the first waveform
        guess = make_average(first[:, 1], files[1:])

        # and then use this guess to make a new average using all the files
        average = make_average(guess, files)

        # construct the output filename
        if pol == "?":
            outname = op.join(avg_dir, 'notches_'+config+'.imp')
        else:
            outname = op.join(avg_dir, 'notches_'+config+f'_{pol}.imp')

        # and save the average
        np.savetxt(
            outname,
            np.vstack((first[:, 0], average)).T,
            header="Time (ns) | Amplitude (V/ns)",
            fmt="%.2f %.8f",
        )
