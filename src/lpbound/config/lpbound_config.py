class LpBoundConfig:
    def __init__(
        self,
        benchmark_name: str = "joblight",
        # A benchmark could have many workloads attached to it, e.g., `joblight-subqueries`, `joblight-joins`.
        workload_file_path: str = None,
        num_mcvs: int = 5000,
        num_buckets: int = 128,
        max_p: int = 10,
        include_l0: bool = True,
        include_l_inf: bool = True,
        enable_groupby: bool = True,
    ):
        self.benchmark_name: str = benchmark_name
        self.workload_file_path: str = workload_file_path
        self.num_mcvs: int = num_mcvs
        self.num_buckets: int = num_buckets
        self.min_p: int = 1
        self.max_p: int = max_p
        self.include_l0: bool = include_l0
        self.include_l_inf: bool = include_l_inf
        self.enable_groupby: bool = enable_groupby

    def __str__(self):
        return f"""
      benchmark_name={self.benchmark_name}
      workload_file_path={self.workload_file_path}
      max_p={self.max_p}
    """
