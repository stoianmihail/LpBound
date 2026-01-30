from collections import defaultdict
from ortools.linear_solver import pywraplp

from lpbound.solver.solver_utils import entropy, sorted_set
from lpbound.utils.types import AliasColPair

# Query utils.
from lpbound.acyclic.join_graph.join_graph import JoinGraph

def create_additivity_lp_variables(
  solver: pywraplp.Solver,
  jg: JoinGraph,
  verbose: bool = False,
) -> tuple[dict[str, pywraplp.Variable], pywraplp.Objective]:
  """
    join_pool_map: `(alias, col_name) -> pool_id`.
    join_pool_alias_map: `alias -> [pool_id]`: map of aliases to the pool_ids they are in.
    relations: list of relations
    create the following variables:
      - for each join pool, we create a variable with the name {pool_index}, such as 1, 2, ...
      - for each alias, we create a variable with the name {0_alias}, such as 0_T, 0_MC, ...
    Then, we create some combinations:
      - for each relation, we create the union of variables in the relation
  """

  # Used to store the variables used in the LP.
  lp_variables = {}

  # The inverse mapping from type to variables.
  lp_type_mapping = {
    'non-join': dict(),
    'full': dict()
  }

  # Update the variables.
  def update_lp_variables(var_name, var_type, var, extra):
    lp_variables[var_name] = {
      'type': var_type,
      'var': var,
      'extra': extra,
    }

    # Only maintain vars that do not represent pools. Match that with the alias!
    if var_type != 'pool':
      assert 'alias' in extra
      lp_type_mapping[var_type][extra['alias']] = var_name

  # Create the variables for the join pools.
  for pool_id in set(jg.join_pool_map.values()):
    str_pool_id = str(pool_id)

    # Update.
    update_lp_variables(str_pool_id, 'pool', solver.NumVar(0, solver.infinity(), str_pool_id), { 'pool-id' : pool_id })

    # Verbose.
    if verbose:
      print(f'Variable {str_pool_id}: {lp_variables[str_pool_id]}.')

  # for each relation,
  # - we create the non-join variables: 0T, 0MC, ...
  # - we create the union of the variables in the relation: 0T_1_2 (if 1 and 2 are in the relation), 0MC_1 (if 1 is in the relation)
    
  full_var_names: list[str] = []
  for alias in jg.vertices:
    non_join_var_name = f'0{alias}'
    assert non_join_var_name not in lp_variables, 'Hmm, seems we hit the challenge of duplicate relations.'

    # Update.
    update_lp_variables(non_join_var_name, 'non-join', solver.NumVar(0, solver.infinity(), non_join_var_name), { 'alias': alias })

    # Verbose.
    if verbose:
      print(f'Variable {non_join_var_name}: {lp_variables[non_join_var_name]['var']}.')

    # For all join pools that contain the alias, we create the union of the variables in the relation.
    pool_ids = jg.join_pool_alias_map[alias]
    full_var_name = entropy(
      sorted_set(
        [non_join_var_name] + [str(pool_id) for pool_id in pool_ids]
      )
    )

    # Update.
    update_lp_variables(full_var_name, 'full', solver.NumVar(0, solver.infinity(), full_var_name), { 'alias': alias })

    # Verbose.
    if verbose:
      print(f'Variable {full_var_name}: {lp_variables[full_var_name]['var']}.')

    # Store it.
    full_var_names.append(full_var_name)

    # add the local monotonicity inequality
    # h(R-vars) >= h(non_join_variable/join_variable)
    # e.g., h(0T_1_2) >= h(0T), h(0MC_1) >= h(0MC), h(0T_1) >= h(1)
    constraint, contraint_id = (
      lp_variables[full_var_name]['var'] >= lp_variables[non_join_var_name]['var'],
      f'Mono Ineq.: H({full_var_name}) >= H({non_join_var_name})',
    )
    if verbose:
      print(f"Constraint {contraint_id}")
    solver.Add(constraint, contraint_id)
    for pool_id in pool_ids:
      constraint, contraint_id = (
        lp_variables[full_var_name]['var'] >= lp_variables[str(pool_id)]['var'],
        f'Mono Ineq.: H({full_var_name}) >= H({str(pool_id)})',
      )
      if verbose:
        print(f'Constraint {contraint_id}.')
      solver.Add(constraint, contraint_id)

    # add the additivity inequality
    # h(R-vars) <= sum_{X in R} h(X)
    # e.g., h(0T_1_2) <= h(0T) + h(1) + h(2)
    lp_variables_in_relation = [lp_variables[non_join_var_name]['var']] + [lp_variables[str(pool_id)]['var'] for pool_id in pool_ids]
    constraint, contraint_id = (
      lp_variables[full_var_name]['var'] <= solver.Sum(lp_variables_in_relation),
      f'Additivity Ineq.: H({full_var_name}) <= H({non_join_var_name}) + '
      + ' + '.join([f'H({str(pool_id)})' for pool_id in pool_ids]),
    )
    if verbose:
      print(f'Constraint {contraint_id}.')
    solver.Add(constraint, contraint_id)

  # create the objective:
  #  sum_{R in relations}h(R-vars) - (# appearances of join_vars)h(join_vars)
  objective_entropy = solver.Objective()
  for full_var_name in full_var_names:
    # Set the coefficient.
    objective_entropy.SetCoefficient(lp_variables[full_var_name]['var'], 1)

  # Build the counts: pool_id -> number of times it appears in the relations.
  pool_id_count: defaultdict[str, int] = defaultdict(int)
  for pool_id in jg.join_pool_map.values():
    pool_id_count[str(pool_id)] += 1

  # Set the entropies for the pool ids.
  for pool_id in pool_id_count:
    lp_var = lp_variables[pool_id]['var']
    count = pool_id_count[pool_id]
    if count > 1:
      objective_entropy.SetCoefficient(lp_var, -(count - 1))
    else:
      assert 0, f'Pool_id {pool_id} appears only once.'
  objective_entropy.SetMaximization()

  if verbose:
    print("---> lp_variables:")
    for key, value in lp_variables.items():
      print(f"Variable {key}: {value['var']}")

  # And return.
  return lp_variables, lp_type_mapping, objective_entropy