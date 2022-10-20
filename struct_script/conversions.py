MIN_FREQUENCY = 50     # frequency on 0 vunits
MAX_FREQUENCY = 20000  # frequency on 1 vunits


def hz_to_vunits(hz: float) -> float:
    return (hz / MIN_FREQUENCY)