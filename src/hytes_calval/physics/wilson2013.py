"""Wilson (2013) skin/bulk temperature model interface.

The actual equations are intentionally not implemented until the controlling
paper has been entered into ``docs/wilson_2013_specification.md`` and checked
against the project team's interpretation.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class WilsonInputs:
    """Candidate inputs whose exact definitions must be confirmed from the paper."""

    bulk_temp_c: float
    wind_speed_mps: float
    air_temp_c: float
    pressure_pa: float
    relative_humidity_pct: float | None = None
    specific_humidity_kgkg: float | None = None
    shortwave_down_wm2: float | None = None
    longwave_down_wm2: float | None = None
    wind_height_m: float | None = None


@dataclass(frozen=True)
class WilsonResult:
    """Auditable output structure for the eventual reference implementation."""

    bulk_temp_c: float
    skin_bulk_correction_c: float
    skin_temp_c: float
    qc_good: bool
    qc_reason: str


def estimate_skin_temperature(inputs: WilsonInputs) -> WilsonResult:
    """Estimate skin temperature using Wilson (2013).

    Raises:
        NotImplementedError: Until the exact paper equations, constants,
        conventions, and validity ranges are verified.
    """
    raise NotImplementedError(
        "Wilson (2013) is not yet implemented. Complete the paper specification, "
        "equation register, variable mapping, and reproduction tests first."
    )
