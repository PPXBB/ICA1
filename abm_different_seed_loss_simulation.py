import numpy as np
import matplotlib.pyplot as plt
from solve_for_flow import solve_for_flow
from cell_migration import cell_migration, caculate_branch_probability
from realign_polarity import realign_polarity
from plot_network import plot_network
from make_segments import make_segments
from abm_ec_simulation_v2 import initialize_segments, compute_conductance
from random_seed_list import *
import copy
import random
import json
from joblib import Parallel, delayed

def store_output(seed, Ncell, D, P1, t):
    # Store results in a dictionary
    result = {
        "Random Seed": int(seed),  # 转换为 Python 的 int 类型
        "Time Step": int(t),       # 转换为 Python 的 int 类型
        "Ncell": [int(n) for n in Ncell],  # 转换为 Python 的 int 类型列表
        "D": [float(d) for d in D],       # 转换为 Python 的 float 类型列表
        "P1": float(P1)                   # 转换为 Python 的 float 类型
    }
    return result

### Run a single simulation with the given random seed and parameters
def run_simulation(seed, Nt, Pin, Pout, mu, Nseg, num_cell, cell_size, branch_rule, branch_alpha, w1, w2, w3, w4, L):

    np.random.seed(seed)  # Set the random seed
    random.seed(seed)
    # Initialize cell and vessel segment properties
    Ncell = np.ones(Nseg) * num_cell
    seg_cells = initialize_segments(Nseg, num_cell)

    # Compute initial conductance and shear stress
    D, G, H = compute_conductance(Nseg, Ncell, cell_size, mu, L)

    # Solve for initial flow
    P, Q, tau = solve_for_flow(G, Pin, Pout, H)

    P1 = caculate_branch_probability(seg_cells, tau, branch_alpha)

    # Store initial state
    time_series_results = []  # Store results for all time steps
    initial_result = store_output(seed, Ncell, D, P1, 0)
    time_series_results.append(initial_result)

    # Time-stepping loop
    for t in range(Nt):
        migrate = np.zeros(Nseg)
        new_seg_cells = copy.deepcopy(seg_cells)

        for seg in range(Nseg):
            seg_cells, new_seg_cells = realign_polarity(seg, Q, seg_cells, new_seg_cells, w1, w2, w3, w4)
            seg_cells, new_seg_cells = cell_migration(seg, seg_cells, new_seg_cells, migrate, Q, branch_rule, branch_alpha, tau)

        seg_cells = copy.deepcopy(new_seg_cells)

        # Update Ncell
        for seg in range(Nseg):
            Ncell[seg] = seg_cells[seg]['num']

        # Update conductance and shear stress
        D, G, H = compute_conductance(Nseg, Ncell, cell_size, mu, L)

        # Solve for updated flow
        P, Q, tau = solve_for_flow(G, Pin, Pout, H)

        P1 = caculate_branch_probability(seg_cells, tau, branch_alpha)
    
        # Store the output of the simulation
        result = store_output(seed, Ncell, D, P1, t+1)
        time_series_results.append(result)

    return time_series_results

# # Initialize empty list to store all results
# all_results = []

# # random_seeds = np.random.randint(0, 1000000000, size=10)  # Generate random seeds for multiple simulations
# print(random_seeds)
# # Run multiple simulations with different random seeds
# for seed in random_seeds:  # Use the generated random seeds
#     print(f"Running simulation with random seed {seed}")
#     seed_results = run_simulation(seed, Nt, Pin, Pout, mu, Nseg, num_cell, cell_size, 
#                                 branch_rule, branch_alpha, w1, w2, w3, w4, L)
#     all_results.extend(seed_results)


# # with open("time_series_results.json", "w") as f:
# #     json.dump(all_results, f, indent=4)
# output_name = "time_series_results_a_" + str(branch_alpha) + ".json"
# with open(output_name, "w") as f:
#     json.dump(all_results, f, indent=1, separators=(',', ':'))

if __name__ == "__main__":
    
    # Input parameters
    Nt = 60  # Number of time steps
    Pin = 100  # Inlet pressure (Pa)
    Pout = 0  # Outlet pressure (Pa)

    mu = 3.5e-3  # Dynamic viscosity of blood (Pa-s)
    Nn = 40  # Number of nodes
    Nseg = 40  # Number of segments
    num_cell = 8  # Initial number of cells per segment
    cell_size = 5e-6  # Size of each cell (m)

    branch_rule = 1  # Branching rule - new
    branch_alpha = 1 # Branching parameter

    # Polarization re-alignment weights
    w2 = 1  # Flow component weight
    w3 = 0  # Neighbor re-alignment weight
    w4 = 0  # Random re-alignment weight
    w1 = 1 - w2 - w3 - w4  # Persistence component

    # Initialize segment properties
    L = np.ones(Nseg) * 10e-6  # Segment lengths (m) ### doubel cell size
    Ncell = np.ones(Nseg) * num_cell  # Segment cell number array
    D = np.zeros(Nseg)  # Segment diameters (m)
    G = np.zeros(Nseg)  # Segment conductance array (m^4/Pa-s-m)
    H = np.zeros(Nseg)  # Shear stress calculation factor


    # Initialize empty list to store all results
    all_results = []

    # random_seeds = np.random.randint(0, 1000000000, size=10)  # Generate random seeds for multiple simulations
    # Run multiple simulations with different random seeds
    for seed in random_seeds[0:10]:  # Use the generated random seeds
        print(f"Running simulation with random seed {seed}")
        seed_results = run_simulation(seed, Nt, Pin, Pout, mu, Nseg, num_cell, cell_size, 
                                    branch_rule, branch_alpha, w1, w2, w3, w4, L)
        all_results.extend(seed_results)
        break


    # with open("time_series_results.json", "w") as f:
    #     json.dump(all_results, f, indent=4)
    output_name = "time_series_results_BR1.json"
    with open(output_name, "w") as f:
        json.dump(all_results, f, indent=1, separators=(',', ':'))


    # # 生成 alpha 值序列，从 0 到 1，步长为 0.05
    # alpha_values = np.arange(0, 1.05, 0.05)

    # import os
    
    # # 创建保存结果的目录
    # output_dir = "Data"
    
    # # 遍历所有 alpha 值
    # for alpha in alpha_values:
    #     print(f"Running simulations for alpha = {alpha:.2f}")
    #     # Initialize empty list to store all results
    #     all_results = []
    
    #     # for seed in random_seeds:  # Use the generated random seeds
    #     #     # print(f"Running simulation with random seed {seed}")
    #     #     seed_results = run_simulation(seed, Nt, Pin, Pout, mu, Nseg, num_cell, cell_size, 
    #     #                             branch_rule, alpha, w1, w2, w3, w4, L)
    #     #     all_results.extend(seed_results)
        
    #     all_results = Parallel(n_jobs=-1)(delayed(run_simulation)
    #                   (seed, Nt, Pin, Pout, mu, Nseg, num_cell, cell_size, branch_rule, alpha, w1, w2, w3, w4, L) 
    #                   for seed in random_seeds)
    #     # 扁平化结果
    #     all_results = [result for sublist in all_results for result in sublist]

    #     # 将结果写入指定目录下的文件
    #     filename = f"1000_seed_time_series_results_a_{alpha:.2f}.json"
    #     filepath = os.path.join(output_dir, filename)
        
    #     with open(filepath, "w") as f:
    #         json.dump(all_results, f, indent=1, separators=(',', ':'))
    #     print(f"Results saved to: {filepath}")
