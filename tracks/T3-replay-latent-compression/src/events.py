"""T3 events: parse the real CA1 linear-track session into population spike-sequence tensors.

Data: nelpy example-data `linear-track` (public), a real hippocampal CA1 session with sorted
spike times (spikes.mat) + video position tracking (trajectory.videoPositionTracking).
Source: github.com/nelpy/example-data. Cached under data/hippocampus/.

What this builds (the "sequences" T3 compresses):
  * per-unit spike trains (list of float time arrays);
  * run-epoch population RATE sequences: for each track traversal, a (n_units, n_bins) matrix
    of binned firing, with units ORDERED by place-field peak location. A correct place-cell
    sequence appears as a diagonal sweep -- that diagonal IS the structure to preserve under
    compression. (This is the awake-run analogue of a replay sequence; the blueprint's replay
    "engram" is exactly such an ordered population sequence.)

Contract:
    Session:
      spikes : list[np.ndarray]     per-unit spike times (s)
      t      : np.ndarray           position sample times (s)
      x      : np.ndarray           linearized position (cm-ish, normalized 0..1)
    sequences(session) -> list of (n_units, n_bins) float arrays, units place-ordered.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import numpy as np
from scipy.io import loadmat

# tracks/T3-replay-latent-compression/src/events.py -> project root is parents[3]
_H = Path(__file__).resolve().parents[3] / "data" / "hippocampus"


@dataclass
class Session:
    spikes: list[np.ndarray]
    t: np.ndarray
    x: np.ndarray            # normalized linear position in [0, 1]


def _as_times(field) -> np.ndarray:
    a = np.asarray(field)
    while a.dtype == object and a.size >= 1:
        a = np.asarray(a.ravel()[0])
    return a.ravel().astype(float) if a.size else np.array([])


def _extract_units(sp, out):
    a = np.asarray(sp)
    if a.dtype.names and "time" in a.dtype.names:
        for elem in a.ravel():
            t = _as_times(elem["time"])
            if t.size:
                out.append(t)
        return
    if a.dtype == object:
        for elem in a.ravel():
            if np.asarray(elem).size:
                _extract_units(elem, out)


def load_dandi(path: Path = _H / "dandi000044_buddy.npz") -> Session:
    """Load a cached DANDI replay session (spike times + linearized position) built by
    scripts/fetch_dandi_replay.py. Richer substrate than the nelpy session (48 pyramidal
    units, proper linearized position, many laps)."""
    d = np.load(path, allow_pickle=True)
    spikes = [np.asarray(s, dtype=float).ravel() for s in d["spike_times"]]
    spikes = [s for s in spikes if s.size > 5]
    t = np.asarray(d["tpos"], dtype=float)
    x = np.asarray(d["pos"], dtype=float)
    ok = ~np.isnan(x)
    t, x = t[ok], x[ok]
    x = (x - x.min()) / (np.ptp(x) + 1e-9)
    return Session(spikes=spikes, t=t, x=x)


def load_session(data_dir: Path = _H) -> Session:
    mat = loadmat(str(data_dir / "spikes.mat"))
    spikes: list[np.ndarray] = []
    _extract_units(mat["spikes"], spikes)
    spikes = [s for s in spikes if s.size > 5]  # drop near-silent units

    raw = (data_dir / "trajectory.bin").read_bytes()
    hdr_end = raw.find(b"<End settings>\n") + len(b"<End settings>\n")
    rec = np.dtype([("time", "<u4"), ("x", "<u2"), ("y", "<u2"), ("x2", "<u2"), ("y2", "<u2")])
    body = raw[hdr_end:]
    pos = np.frombuffer(body[: (len(body) // rec.itemsize) * rec.itemsize], dtype=rec)

    # position clock is 30 kHz per header; convert to seconds and align to spike time base
    tpos = pos["time"].astype(np.float64) / 30000.0
    x = pos["x"].astype(np.float64)
    # restrict to the window where spikes exist
    allt = np.concatenate(spikes)
    lo, hi = allt.min(), allt.max()
    m = (tpos >= lo) & (tpos <= hi)
    tpos, x = tpos[m], x[m]
    if tpos.size < 100:  # clock mismatch fallback: just normalize position over its own span
        tpos = np.linspace(lo, hi, pos.size)
        x = pos["x"].astype(np.float64)
    # normalize position to [0,1]
    x = (x - x.min()) / (np.ptp(x) + 1e-9)
    return Session(spikes=spikes, t=tpos, x=x)


def _place_order(session: Session, n_bins_space: int = 20) -> np.ndarray:
    """Order units by the track location of their peak firing (place-field center)."""
    edges = np.linspace(0, 1, n_bins_space + 1)
    centers = 0.5 * (edges[:-1] + edges[1:])
    peak_loc = []
    for s in session.spikes:
        xi = np.interp(s, session.t, session.x, left=np.nan, right=np.nan)
        xi = xi[~np.isnan(xi)]
        if xi.size == 0:
            peak_loc.append(0.5)
            continue
        hist, _ = np.histogram(xi, bins=edges)
        peak_loc.append(centers[int(np.argmax(hist))])
    return np.argsort(peak_loc)


def run_epochs(session: Session, min_dur: float = 1.0, speed_thresh: float = 0.02):
    """Split into track-traversal epochs where the animal is moving (|dx/dt| above threshold)."""
    t, x = session.t, session.x
    if t.size < 10:
        return []
    dt = np.gradient(t)
    v = np.abs(np.gradient(x) / (dt + 1e-9))
    moving = v > speed_thresh
    epochs = []
    i = 0
    while i < len(moving):
        if moving[i]:
            j = i
            while j < len(moving) and moving[j]:
                j += 1
            if t[j - 1] - t[i] >= min_dur:
                epochs.append((t[i], t[j - 1]))
            i = j
        else:
            i += 1
    return epochs


def windowed_sequences(session: Session, win_s: float = 1.5, stride_s: float = 0.5,
                       n_bins: int = 25, n_bins_space: int = 20, min_span: float = 0.3,
                       min_spikes: int = 20):
    """Many overlapping population-sequence windows during movement (for a trainable sample).

    A single session has few clean full laps (too few to train an AE + held-out sweep). The
    blueprint's 'replay sequence' is a population activity sequence, not necessarily a full lap,
    so we tile running periods with overlapping windows. Each window that covers enough track
    span and spikes becomes a place-ordered (n_units, n_bins) sequence. Yields hundreds of
    real samples while keeping the decode-based trajectory content.
    """
    order = _place_order(session, n_bins_space)
    t, x = session.t, session.x
    if t.size < 10:
        return []
    t0_all, t1_all = t.min(), t.max()
    seqs = []
    start = t0_all
    while start + win_s <= t1_all:
        t0, t1 = start, start + win_s
        start += stride_s
        m = (t >= t0) & (t <= t1)
        if m.sum() < 3 or np.ptp(x[m]) < min_span:
            continue
        edges = np.linspace(t0, t1, n_bins + 1)
        mat = np.zeros((len(session.spikes), n_bins))
        for u, s in enumerate(session.spikes):
            sub = s[(s >= t0) & (s < t1)]
            if sub.size:
                h, _ = np.histogram(sub, bins=edges)
                mat[u] = h
        if mat.sum() >= min_spikes:
            seqs.append(mat[order])
    return seqs


def _traversal_span(session: Session, t0: float, t1: float) -> float:
    """Fraction of the linear track the animal actually covers during [t0, t1)."""
    m = (session.t >= t0) & (session.t <= t1)
    if m.sum() < 3:
        return 0.0
    xs = session.x[m]
    return float(np.ptp(xs))


def _net_direction(session: Session, t0: float, t1: float) -> int:
    """+1 if net rightward traversal over [t0,t1), -1 if leftward, 0 if ambiguous."""
    m = (session.t >= t0) & (session.t <= t1)
    if m.sum() < 3:
        return 0
    xs = session.x[m]
    d = xs[-1] - xs[0]
    return 1 if d > 0 else (-1 if d < 0 else 0)


def laps(session: Session, min_span: float = 0.6, min_dur: float = 1.0, direction: int = 0):
    """(Near-)full track traversals (span >= min_span). If `direction` in {+1,-1}, keep only
    laps in that running direction.

    Direction-splitting is standard in replay analysis: on a linear track the animal runs both
    ways, and pooling directions makes place-field decoding ambiguous (a cell fires at the same
    position in both directions). Separating by direction is required for clean decode content.
    """
    out = []
    for (t0, t1) in run_epochs(session, min_dur=min_dur, speed_thresh=0.008):
        if _traversal_span(session, t0, t1) < min_span:
            continue
        if direction != 0 and _net_direction(session, t0, t1) != direction:
            continue
        out.append((t0, t1))
    return out


def sequences(session: Session, n_bins: int = 25, n_bins_space: int = 20,
              min_span: float = 0.6, use_laps: bool = True, direction: int = 0):
    """Place-ordered (n_units, n_bins) population rate matrices, one per clean lap (default).

    `direction` in {+1,-1} restricts to one running direction (recommended for clean decode).
    """
    order = _place_order(session, n_bins_space)
    epochs = laps(session, min_span=min_span, direction=direction) if use_laps else run_epochs(session)
    seqs = []
    for (t0, t1) in epochs:
        edges = np.linspace(t0, t1, n_bins + 1)
        mat = np.zeros((len(session.spikes), n_bins))
        for u, s in enumerate(session.spikes):
            sub = s[(s >= t0) & (s < t1)]
            if sub.size:
                h, _ = np.histogram(sub, bins=edges)
                mat[u] = h
        mat = mat[order]                        # place-order rows
        if mat.sum() > 0:
            seqs.append(mat)
    return seqs
