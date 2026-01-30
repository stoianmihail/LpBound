from dataclasses import dataclass
from typing import Tuple, Union
from enum import Enum
import subprocess
import pyodbc
import duckdb
import json
import sys
import os

# LpBound config.
from lpbound.config.paths import LpBoundPaths
from lpbound.config.lpbound_config import LpBoundConfig

def get_duckdb_db_path(lpbound_config: LpBoundConfig):
  return os.path.join('dbs', f'{LpBoundPaths.WORKLOAD_TO_DB_MAP[lpbound_config.benchmark_name]}.duckdb')

class ConnectionWrapper:
  def __init__(
    self,
    lpbound_config: LpBoundConfig,
    read_only: bool,
  ):
    # Set.
    self.lpbound_config = lpbound_config
    self.read_only = read_only

    # Reset the connection.
    self.con = None

    # Open the database connection.
    self.open()

  def exec(self, query):
    # print(f'[exec] {query}')
    assert self.con is not None
    # print(f'[exec] Query:\n{query}')

    # And try.
    try:
      self.con.sql(query)
    except Exception as e:
      print(e)
      sys.exit(-1)
  
  def fetchone(self, query):
    # print(f'[fetchone] Query:\n{query}')
    assert self.con is not None
    try:
      return self.con.sql(query).fetchone()
    except Exception as e:
      print(e)
      sys.exit(-1)

  def fetchall(self, query):
    # print(f'[fetchall]')
    assert self.con is not None
    # print(f'[fetchall] Query:\n{query}')
    return self.con.sql(query).fetchall()

  def fetchdf(self, query):
    # print(f'[fetchdf]')
    assert self.con is not None
    # print(f'[fetchall] Query:\n{query}')
    return self.con.sql(query).fetchdf()

  def open(self):
    # And create the connection.
    self.con = duckdb.connect(
      get_duckdb_db_path(self.lpbound_config),
      read_only = self.read_only
    )

  def close(self):
    if self.con is not None:
      self.con.close()
