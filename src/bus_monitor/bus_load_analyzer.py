from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd


def analyze(
    log_path: Path,
    bitrate: int = 500_000,
) -> dict:

    df = pd.read_csv(log_path)

    if df.empty:
        return {
            "frames": 0,
            "duration_s": 0.0,
            "frame_rate": 0.0,
        }

    df["timestamp"] = pd.to_numeric(
        df["timestamp"]
    )

    duration = (
        df["timestamp"].max()
        - df["timestamp"].min()
    )

    if duration <= 0:
        frame_rate = 0.0
    else:
        frame_rate = (
            len(df) / duration
        )

    result = {
        "frames": len(df),
        "duration_s": duration,
        "frame_rate": frame_rate,
        "bitrate": bitrate,
    }

    for can_id, group in df.groupby("can_id"):

        if len(group) < 2:
            continue

        timestamps = (
            group["timestamp"]
            .sort_values()
            .diff()
            .dropna()
        )

        result[
            f"{can_id}_mean_period_ms"
        ] = timestamps.mean() * 1000

        result[
            f"{can_id}_max_period_ms"
        ] = timestamps.max() * 1000

        result[
            f"{can_id}_min_period_ms"
        ] = timestamps.min() * 1000

    return result


def main() -> None:

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "log",
        type=Path,
    )

    parser.add_argument(
        "--bitrate",
        type=int,
        default=500_000,
    )

    args = parser.parse_args()

    report = analyze(
        args.log,
        args.bitrate,
    )

    print("\nCAN BUS ANALYSIS")
    print("================")

    for key, value in report.items():

        if isinstance(value, float):
            print(
                f"{key:30s}: "
                f"{value:.3f}"
            )

        else:
            print(
                f"{key:30s}: "
                f"{value}"
            )


if __name__ == "__main__":
    main()
