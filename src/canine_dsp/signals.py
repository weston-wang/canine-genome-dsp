import numpy as np

EIIP = {"A": 0.1260, "C": 0.1340, "G": 0.0806, "T": 0.1335, "N": 0.0}


def indicator(sequence: str, base: str) -> np.ndarray:
    """Binary nucleotide indicator signal."""
    chars = np.frombuffer(sequence.upper().encode("ascii"), dtype="S1")
    return (chars == base.upper().encode("ascii")).astype(float)


def eiip(sequence: str) -> np.ndarray:
    """EIIP numerical representation; ambiguous N maps to zero."""
    return np.fromiter((EIIP[b] for b in sequence.upper()), dtype=float)


def windowed_gc(sequence: str, window: int) -> np.ndarray:
    if window <= 0:
        raise ValueError("window must be positive")
    n = len(sequence) // window
    if n == 0:
        raise ValueError("sequence is shorter than one window")
    chars = np.frombuffer(sequence[: n * window].upper().encode(), dtype="S1").reshape(n, window)
    valid = chars != b"N"
    gc = (chars == b"G") | (chars == b"C")
    return np.divide(gc.sum(1), valid.sum(1), out=np.full(n, np.nan), where=valid.sum(1) > 0)


def variant_density(positions_1based: np.ndarray, length: int, window: int) -> np.ndarray:
    """Variant counts per non-overlapping window."""
    if window <= 0 or length <= 0:
        raise ValueError("length and window must be positive")
    edges = np.arange(0, length + window, window)
    positions_0based = np.asarray(positions_1based) - 1
    positions_0based = positions_0based[(positions_0based >= 0) & (positions_0based < length)]
    return np.histogram(positions_0based, bins=edges)[0].astype(float)

