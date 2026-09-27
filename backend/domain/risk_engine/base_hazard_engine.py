"""Hazard-engine abstraction.

Every hazard engine (heat, and later flood/drought/water-stress) implements:

    compute_risk(hazard_layer, exposure_layer, vulnerability_layer, config) -> RiskLayer

New hazards are added by implementing this interface — never by special-casing
a hazard in the API, Optimizer, or AI layers. See docs/climate-risk-engine.md.
"""
