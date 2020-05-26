from abc import ABC, abstractmethod
from typing import List

import xarray as xr

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
        """
        The list of available channels on this flight.
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
        """
        The list of available phi sectors on this flight.

        These should be numbered from 0 to N.
        """

    @property
    @abstractmethod
    def rings(self) -> List[str]:
        """
        The list of ringss for this payload.

        This should be one-letter identifiers (T, M, B, etc.)
        """

    @property
    def pols(self) -> List[str]:
        """
        The available polarizations of this payload.

        This currently returns ["H", "V"] for all payloads.
        """
        return ["H", "V"]

    @property
    def digitizer_responses(self) -> xr.DataArray:
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
    def trigger_responses(self) -> xr.DataArray:
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

    def digitizer_response(self, channel: str, config: str) -> xr.DataArray:
        """
        Load the digitizer response for a given
        channel/config for this flight.

        Parameters
        ----------
        None

        Returns
        -------
        response:
            The response for `channel`+`config.

        Raises
        ------
        ValueError:
            If `channel` and `config` are not valid for this flight.`
        """

        # check that we have a valid config
        if config not in self.configs or channel not in self.channels:
            raise ValueError(f"{channel} and {config} not valid for this flight.")

        # if so, return the response
        return panama.responses.get_digitizer_response(channel, config, self.flight)

    def trigger_response(self, channel: str, config: str) -> xr.DataArray:
        """
        Load the trigger response for a given
        channel/config for this flight.

        Parameters
        ----------
        None

        Returns
        -------
        response:
            The response for `channel`+`config.

        Raises
        ------
        ValueError:
            If `channel` and `config` are not valid for this flight.`
        """

        # check that we have a valid config
        if config not in self.configs or channel not in self.channels:
            raise ValueError(f"{channel} and {config} not valid for this flight.")

        # if so, return the response
        return panama.responses.get_trigger_response(channel, config, self.flight)
