"""Shared substrate for the mind-migration research program.

Modules:
    connectome : dataset loaders (C. elegans real-data hook + deterministic synthetic fallback)
    model      : baseline connectome-driven functional model
    fps        : Functional Preservation Score metric + benchmark harness
    compress   : compression operations (pruning + quantization)

Dependency direction: tracks import from `shared`; `shared` never imports from tracks.
"""

from . import connectome, model, fps, compress  # noqa: F401
