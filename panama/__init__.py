__version__ = "0.0.1"

import enum
from . import responses  # noqa: F401


@enum.unique
class Ring(enum.IntEnum):
    """An identifier for an antenna ring.
    """

    Top = 0
    Middle = 1
    Bottom = 2


class Pol(enum.IntEnum):
    """An identifier for a waveform polarization.

    You should either use Horizontal & Vertical or
    LeftCircular and RightCircular buth do not mix both
    as they represent the same indices.
    """

    Horizontal = 0
    Vertical = 1

    LeftCircular = 0
    RightCircular = 1

    # the number of supported polarizations
    N = 2
