from abc import ABC, abstractmethod
from typing import Dict, List

import numpy as np

import panama.responses


class ANITA(ABC):
    """A class representing a general ANITA/PUEO flight.

    This an abstract class to encapsulate common methods for ANITA and PUEO
    flights. This cannot be instantiated directly - please use one of the
    flight-specific subclasses.
    """

    # the flight number for this flight
    flight: int

    @property
    @abstractmethod
    def channels(self) -> List[str]:
        """The list of available channels on this flight.
        """

    @property
    @abstractmethod
    def configs(self) -> List[str]:
        """
        The list of available configurations.
        """

    @property
    @abstractmethod
    def sectors(self) -> List[int]:
        """The list of available phi sectors on this flight.

        These should be numbered from 0 to N.
        """

    @property
    def digitizer_responses(self) -> Dict[str, Dict[str, np.ndarray]]:
        """
        Load the digitizer responses for this flight.

        This is cached by panama.responses so shoud be loaded
        relatively quickly.

        Parameters
        ----------
        None

        Returns
        -------
        responses:
            The full-set of digitizer responses.
        """
        return panama.responses.get_all_responses(
            "digitizer", self.channels, self.configs, self.flight
        )

    @property
    def trigger_responses(self) -> Dict[str, Dict[str, np.ndarray]]:
        """
        Load the trigger responses for this flight.

        This is cached by panama.responses so shoud be loaded
        relatively quickly.

        Parameters
        ----------
        None

        Returns
        -------
        responses:
            The full-set of digitizer responses.
        """
        return panama.responses.get_all_responses(
            "trigger", self.channels, self.configs, self.flight
        )
