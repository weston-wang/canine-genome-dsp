"""Conversation-sourced reference modules on primary intracranial histiocytic sarcoma
in a predisposed dog breed.

Three self-contained, pure-Python modules, each distilled from the research
conversation (not from any prior code):

- ``therapies``     -- every therapy and drug discussed, grouped by class, with per-agent status.
- ``disease``       -- the disease itself: sites, escape routes, mechanisms, and delivery routes.
- ``presentation``  -- what is distinctive about this breed's presentation, biologically and genomically.

The consolidated plain-language report lives in ``docs/CONSOLIDATED_REPORT.md``.

The scientific / DSP / genomics models and the quantitative therapy engine live alongside these
as submodules (``canine_dsp.alphafold``, ``canine_dsp.pharmacology``, ``canine_dsp.core`` ...).
They are imported on demand rather than here, so ``import canine_dsp`` stays free of the heavy
scientific stack (numpy/scipy/torch/...).

This is an analysis, not veterinary advice.
"""

from . import disease, presentation, therapies

__version__ = "0.3.0"

__all__ = ["disease", "presentation", "therapies"]
