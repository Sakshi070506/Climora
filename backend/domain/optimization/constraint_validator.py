"""Non-bypassable gate: the ONLY path by which an optimizer result is persisted
   or returned to the API. Rejects (and logs) any portfolio that violates a hard
   constraint, has negative costs, or exceeds resource availability -- never
   rounds or fixes up a near-miss result. See AGENTS.md section 2.
"""
