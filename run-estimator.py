import argparse
import json
import os

# Configuration logic.
from lpbound.config.paths import LpBoundPaths
from lpbound.config.lpbound_config import LpBoundConfig

# Lpbound logic.
from lpbound.acyclic.lpbound import estimate

# Common utils.
from lpbound.utils import common

# Schema utils.
from lpbound.config.benchmark_schema import load_benchmark_schema, BenchmarkSchema

# Connection utils.
from lpbound.utils.conn_utils import ConnectionWrapper

OUTPUT_ROOT_DIR = './est'

def run_lpbound(lpbound_config, workload_name, workload):
  # Load the schema.
  schema_data: BenchmarkSchema = load_benchmark_schema(lpbound_config)

  # Init the database connection.
  conn_wrapper = ConnectionWrapper(
    lpbound_config, 
    read_only = True,
  )

  with open(f'{OUTPUT_ROOT_DIR}/{lpbound_config.benchmark_name}/lpbound-{lpbound_config.max_p}::{workload_name}.jsonl', 'w') as f:
    # And iterate.
    for query in workload:
      print(f'Estimating {query['tag']}..')
      
      # Estimate.
      est = estimate(
        conn_wrapper,
        schema_data,
        input_query_sql=query['sql'],
        config=lpbound_config,
      )
      # elapsed_ms = (time.perf_counter() - start) * 1000.0
      # print(f'Lpbound executed in {elapsed_ms:.3f} ms.')

      # And dump.
      query[f'lpbound-{lpbound_config.max_p}'] = est
      f.write(
        json.dumps(
          query
        ) + '\n'
      )

def main():
  """Entry point for console script."""
  parser = argparse.ArgumentParser(description='Run xBound.')
  parser.add_argument('estimator', type=str, help='The estimator.')
  parser.add_argument('workload_name', type=str, help='The workload name.')

  args = parser.parse_args()

  # Infer the benchmark name.
  assert '-' in args.workload_name
  benchmark_name = args.workload_name.split('-')[0]

  # Init the config.
  config = LpBoundConfig(
    benchmark_name=benchmark_name,
    workload_file_path=os.path.join(LpBoundPaths.WORKLOADS_DIR, benchmark_name, f'{args.workload_name.replace('.jsonl', '')}.jsonl')
  )

  assert config.workload_file_path is not None
  workload = common.read_jsonl(config.workload_file_path)

  # Infer the workload name.
  workload_name = os.path.basename(config.workload_file_path).replace('.jsonl', '')

  # Ensure `./est/{lpbound_config.benchmark_name}` exists, so that we can always write there.
  benchmark_dir = os.path.join(OUTPUT_ROOT_DIR, config.benchmark_name)
  os.makedirs(benchmark_dir, exist_ok=True)

  # And run.
  run_lpbound(config, workload_name, workload) 
  return

if __name__ == '__main__':
  main()