import argparse
import shutil
import os

# Lpbound utils.
from lpbound.config.paths import LpBoundPaths
from lpbound.config.lpbound_config import LpBoundConfig
from lpbound.acyclic.stat_generator.sql_utils import SqlCommand
from lpbound.acyclic.stat_generator.sql_statistics_generator import (
    generate_all_sql_for_benchmark,
)

# Common utils.
from lpbound.utils import common


def main(lpbound_config):
    import duckdb

    db_path = os.path.join(
        "dbs", f"{LpBoundPaths.WORKLOAD_TO_DB_MAP[config.benchmark_name]}.duckdb"
    )
    assert os.path.exists(db_path)
    con = duckdb.connect(db_path, read_only=True)

    # 3) Generate the Lp-norm SQL commands
    cmds: list[SqlCommand] = generate_all_sql_for_benchmark(con, lpbound_config)

    print(cmds)
    # 3a) write the commands to a file for inspection
    # groupby_suffix = '_groupby' if lpbound_config.enable_groupby else ''

    # And dump.
    common.safe_write(
        f"./dump/{config.benchmark_name}/lpbound/lpbound-norms.sql",
        "\n".join(cmd["sql"] for cmd in cmds),
    )


if __name__ == "__main__":
    # Init a default config.
    lpbound_config = LpBoundConfig()

    parser = argparse.ArgumentParser(
        description="Generate SQL dumps for the `NORMS_TABLE` table."
    )
    parser.add_argument(
        "benchmark_name", type=str, help="The benchmark to build Lpbound for."
    )
    parser.add_argument(
        "--p-max",
        type=int,
        default=lpbound_config.max_p,
        help=f"Max. p-norm (default: {lpbound_config.max_p})",
    )
    parser.add_argument(
        "--num-mcvs",
        type=int,
        default=lpbound_config.num_mcvs,
        help=f"Number of most common values to consider (default: {lpbound_config.num_mcvs})",
    )
    parser.add_argument(
        "--num-buckets",
        type=int,
        default=lpbound_config.num_buckets,
        help=f"The number of buckets to consider in range predicates (default: {lpbound_config.num_buckets})",
    )
    args = parser.parse_args()

    # Create the new config.
    del lpbound_config
    config = LpBoundConfig(
        benchmark_name=args.benchmark_name,
        num_mcvs=args.num_mcvs,
        num_buckets=args.num_buckets,
        max_p=args.p_max,
    )

    # Make sure we have an empty dump.
    shutil.rmtree(f"dump/{config.benchmark_name}/lpbound", ignore_errors=True)

    # And run.
    main(config)
