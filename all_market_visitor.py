import math
from typing import List, Optional, Tuple
import numpy as np
import pandas as pd


def _euclid(a: Tuple[float, float], b: Tuple[float, float]) -> float:
    dx, dy = a[0] - b[0], a[1] - b[1]
    return math.hypot(dx, dy)


def _pairwise_dist_matrix(coords: np.ndarray) -> np.ndarray:
    # coords: (N,2)
    # returns (N,N) symmetric distance matrix
    diff = coords[:, None, :] - coords[None, :, :]
    return np.sqrt((diff ** 2).sum(axis=2))


def _nearest_neighbor_tour(D: np.ndarray, start_idx: int) -> List[int]:
    n = D.shape[0]
    unvisited = set(range(n))
    tour = [start_idx]
    unvisited.remove(start_idx)
    cur = start_idx
    while unvisited:
        nxt = min(unvisited, key=lambda j: D[cur, j])
        tour.append(nxt)
        unvisited.remove(nxt)
        cur = nxt
    return tour


def _two_opt_once(tour: List[int], D: np.ndarray) -> Tuple[List[int], bool]:
    """Perform a single improvement pass; returns (new_tour, improved?)."""
    n = len(tour)
    best = tour
    improved = False

    def seg_len(i1, i2):
        a, b = best[i1], best[(i1 + 1) % n]
        c, d = best[i2], best[(i2 + 1) % n]
        return D[a, b] + D[c, d]

    for i in range(n - 2):
        for k in range(i + 2, n - (0 if i > 0 else 1)):
            before = seg_len(i, k)
            after = D[best[i], best[k]] + D[best[i + 1], best[(k + 1) % n]]
            if after + 1e-12 < before:
                best = best[: i + 1] + list(reversed(best[i + 1 : k + 1])) + best[k + 1 :]
                improved = True
    return best, improved


def _two_opt(tour: List[int], D: np.ndarray, max_iters: int = 50) -> List[int]:
    cur = tour
    for _ in range(max_iters):
        cur, improved = _two_opt_once(cur, D)
        if not improved:
            break
    return cur


def all_market_visitor(
    markets_df: pd.DataFrame,
    start_waypoint: Optional[str] = None,
    return_to_start: bool = False,
    improve_2opt: bool = True,
) -> pd.DataFrame:
    """
    Build a visit order that covers all markets with short total travel.

    Parameters
    ----------
    markets_df : DataFrame with columns ['waypoint', 'x', 'y']
    start_waypoint : optional waypoint symbol to start at.
                     If None, picks the market with smallest (x, then y).
    return_to_start : if True, closes the tour back to the start.
    improve_2opt : run a 2-opt local improvement after nearest-neighbor.

    Returns
    -------
    route_df : DataFrame with columns:
        - visit_idx (0..N-1 or 0..N if returning to start)
        - waypoint
        - x, y
        - leg_distance (0 for first row)
        - cumulative_distance
    """
    if markets_df.empty:
        return pd.DataFrame(columns=["visit_idx", "waypoint", "x", "y", "leg_distance", "cumulative_distance"])

    for col in ["waypoint", "x", "y"]:
        if col not in markets_df.columns:
            raise ValueError(f"markets_df must contain column '{col}'")

    df = markets_df[["waypoint", "x", "y"]].copy().reset_index(drop=True)
    coords = df[["x", "y"]].to_numpy(dtype=float)
    D = _pairwise_dist_matrix(coords)

    # Pick start index
    if start_waypoint is not None:
        if start_waypoint not in set(df["waypoint"]):
            raise ValueError(f"start_waypoint '{start_waypoint}' not found in markets_df['waypoint']")
        start_idx = int(df.index[df["waypoint"] == start_waypoint][0])
    else:
        # Default: left-most (min x), tie-breaker min y
        start_idx = int(df.sort_values(["x", "y"]).index[0])

    # Build initial tour and optionally improve
    tour = _nearest_neighbor_tour(D, start_idx)
    if improve_2opt and len(tour) >= 4:
        tour = _two_opt(tour, D)

    # Optionally close the tour by returning to start
    sequence = tour + ([tour[0]] if return_to_start else [])

    # Compute leg distances & cumulative
    legs = [0.0]
    cum = [0.0]
    for i in range(1, len(sequence)):
        a, b = sequence[i - 1], sequence[i]
        dist = D[a, b]
        legs.append(dist)
        cum.append(cum[-1] + dist)

    out = df.iloc[sequence].reset_index(drop=True)
    out.insert(0, "visit_idx", range(len(sequence)))
    out["leg_distance"] = np.round(legs, 3)
    out["cumulative_distance"] = np.round(cum, 3)
    return out


# -------------------------
# Minimal example usage
# -------------------------
if __name__ == "__main__":
    # Fake data
    markets = pd.DataFrame(
        {
            "waypoint": [f"M{i:02d}" for i in range(10)],
            "x": [1, 5, 3, 8, 2, 9, 4, 7, 6, 0],
            "y": [0, 2, 7, 1, 6, 5, 9, 3, 4, 8],
        }
    )

    route = all_market_visitor(
        markets_df=markets,
        start_waypoint=None,      # or e.g., "M00"
        return_to_start=False,    # set True to make a loop
        improve_2opt=True,
    )

    print(route)
    print("\nTotal distance:", route["cumulative_distance"].iloc[-1])
