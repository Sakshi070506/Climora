"""Adaptation Portfolio Optimizer (OR-Tools/PuLP, MILP).

Proposes a portfolio given risk + exposure + vulnerability + intervention
catalog + constraints + objective. Does NOT persist results directly --
see constraint_validator.py, the only non-bypassable path to persistence.
"""
