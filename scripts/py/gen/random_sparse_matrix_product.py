#!/usr/bin/env python3
"""Generate two sparse random matrices, multiply them, and report output density.

The script stores both input matrices in COO format as CSV files.
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

import numpy as np
import scipy.sparse as sp


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Generate sparse random matrices A and B, compute A @ B, and report "
            "the density of the output matrix."
        )
    )

    parser.add_argument(
        "--m", type=int, required=True, help="Number of rows of matrix A"
    )
    parser.add_argument(
        "--k", type=int, required=True, help="Shared dimension (A columns, B rows)"
    )
    parser.add_argument(
        "--n", type=int, required=True, help="Number of columns of matrix B"
    )

    parser.add_argument(
        "--sparsity-a",
        type=float,
        default=0.95,
        help="Sparsity of A in [0, 1], where 1.0 means all zeros (default: 0.95)",
    )
    parser.add_argument(
        "--sparsity-b",
        type=float,
        default=0.95,
        help="Sparsity of B in [0, 1], where 1.0 means all zeros (default: 0.95)",
    )

    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("output/sparse_matrices"),
        help="Directory where CSV files are written (default: output/sparse_matrices)",
    )
    parser.add_argument(
        "--a-filename",
        type=str,
        default="matrix_a_coo.csv",
        help="Output CSV filename for matrix A (default: matrix_a_coo.csv)",
    )
    parser.add_argument(
        "--b-filename",
        type=str,
        default="matrix_b_coo.csv",
        help="Output CSV filename for matrix B (default: matrix_b_coo.csv)",
    )
    parser.add_argument(
        "--seed", type=int, default=42, help="Random seed (default: 42)"
    )

    args = parser.parse_args()

    for name in ("m", "k", "n"):
        value = getattr(args, name)
        if value <= 0:
            raise ValueError(f"--{name} must be > 0, got {value}")

    for name in ("sparsity_a", "sparsity_b"):
        value = getattr(args, name)
        if not (0.0 <= value <= 1.0):
            raise ValueError(
                f"--{name.replace('_', '-')} must be in [0, 1], got {value}"
            )

    return args


def generate_sparse_matrix(
    rows: int, cols: int, sparsity: float, rng: np.random.Generator
) -> sp.coo_matrix:
    density = 1.0 - sparsity
    return sp.random(
        rows,
        cols,
        density=density,
        format="coo",
        random_state=rng,
        data_rvs=lambda nnz: rng.random(nnz),
    )


def write_coo_csv(matrix: sp.spmatrix, output_path: Path) -> None:
    coo = matrix.tocoo()
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["row", "col", "value"])
        writer.writerows(zip(coo.row.tolist(), coo.col.tolist(), coo.data.tolist()))


def matrix_density(matrix: sp.spmatrix) -> float:
    rows, cols = matrix.shape
    return matrix.nnz / (rows * cols)


def main() -> None:
    args = parse_args()
    rng = np.random.default_rng(args.seed)

    matrix_a = generate_sparse_matrix(args.m, args.k, args.sparsity_a, rng)
    matrix_b = generate_sparse_matrix(args.k, args.n, args.sparsity_b, rng)

    matrix_c = matrix_a @ matrix_b
    output_density = matrix_density(matrix_c)

    output_dir = args.output_dir
    a_path = output_dir / args.a_filename
    b_path = output_dir / args.b_filename

    write_coo_csv(matrix_a, a_path)
    write_coo_csv(matrix_b, b_path)

    print(
        f"A shape: {matrix_a.shape}, nnz: {matrix_a.nnz}, density: {matrix_density(matrix_a):.6f}"
    )
    print(
        f"B shape: {matrix_b.shape}, nnz: {matrix_b.nnz}, density: {matrix_density(matrix_b):.6f}"
    )
    print(
        f"C shape: {matrix_c.shape}, nnz: {matrix_c.nnz}, density: {output_density:.6f}"
    )
    print(f"Wrote A (COO CSV): {a_path}")
    print(f"Wrote B (COO CSV): {b_path}")


if __name__ == "__main__":
    main()
