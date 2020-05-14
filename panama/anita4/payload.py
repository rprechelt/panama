from typing import List

from cached_property import cached_property

__all__ = ["ANITA4"]


class ANITA4:
    """
    Represent the fourth flight of ANITA.
    """

    flight: int = 4  # the flight that we simulate

    @cached_property
    def channels(self) -> List[str]:
        """
        The list of available channels.

        This is cached so that it is only computed once.
        """
        # The channel identifiers for ANITA-4
        channels: List[str] = []

        # build the channel list
        for phi in range(1, 17):
            for pol in ["H", "V"]:
                for ring in ["T", "M", "B"]:
                    channels.append(f"{phi:02}{ring}{pol}")

        # and return the channels
        return channels

    @property
    def configs(self) -> List[str]:
        """
        The list of available configurations.
        """
        # the configs available in ANITA-4
        configs: List[str] = [
            "260_0_0",
            "260_0_460",
            "260_365_0",
            "260_375_0",
            "260_385_0",
            "260_375_460",
        ]

        # and we are done
        return configs

    @property
    def sectors(self) -> List[int]:
        """
        The list of phi sectors.
        """
        return list(range(1, 17))
