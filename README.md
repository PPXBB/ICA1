# ABM Simulation of Flow-Endothelial Cell Coupling and Bifurcation Stability

This repository contains Python code for an Agent-Based Model (ABM) simulating the migration of endothelial cells (ECs) within a simplified vascular network, focusing on the stability of bifurcations under different cell migration rules.

This work was completed as part of a mini-project based on the concepts presented in:

*   Edgar, L. T., et al. (2021). Bifurcation analysis of a lattice-based model for endothelial cell migration: Macroscopic BAE Systems study. *PLOS Computational Biology*, *17*(3), e1007715.

## Project Overview

The simulation models ECs as agents moving within a predefined network graph consisting of 40 segments. Key aspects simulated include:

*   **Agent Polarity:** ECs align their polarity based on local flow direction.
*   **Network Flow:** Hemodynamics (pressure, flow, shear stress) are calculated based on segment diameter, which dynamically changes with the number of ECs present (`D ~ Ncell`).
*   **Cell Migration:** ECs move between connected segments based on their polarity.
*   **Bifurcation Rules:** Specific rules govern how ECs choose between daughter branches at a key bifurcation (segment 15 leading to 14 and 39). This implementation includes:
    *   **BR1:** Choice based solely on higher Wall Shear Stress (WSS).
    *   **BR2:** Random 50/50 choice.
    *   **BR3:** Choice based on a weighted probability (`alpha` parameter) balancing relative WSS and relative cell number (`Ncell`) in the daughter branches.

## Code Structure

The simulation logic is modularized into several Python scripts:

*   `make_segments.py`: Defines the network topology (segment connections and coordinates).
*   `solve_for_flow.py`: Calculates pressure, flow (Q), and Wall Shear Stress (tau) across the network using conductance derived from segment properties (Ncell -> Diameter -> Conductance).
*   `realign_polarity.py`: Updates the polarity vector for each EC agent based on flow and other potential factors (though primarily flow-driven in this setup).
*   `cell_migration.py`: Implements the movement of EC agents between segments, including the specific logic for the chosen bifurcation rule (BR1, BR3, or BR5) at the junction of segment 15 -> 14/39.
*   `abm_ec_simulation_v2.py`: The main script to run a *single* simulation instance. Initializes the system, runs the time-stepping loop (flow calculation, polarity update, migration), and includes basic plotting functionality (optional).
*   `abm_different_seed_loss_simulation.py`: A script designed to run *multiple* simulation instances with varying random seeds and/or parameters (like `branch_alpha` for BR5). It saves simulation results (e.g., Ncell, Diameter per segment over time) to JSON files for later analysis (e.g., calculating stability percentages).
*   `plot_network.py`: (If used) Utility functions for visualizing the network state.
*   `random_seed_list.py`: (Not provided, **required** by `abm_different_seed_loss_simulation.py`) A file expected to contain a list of integer random seeds used to ensure reproducibility across multiple runs. You will need to create this file (e.g., `random_seeds = [1, 2, 3, ..., 100]`).

## Requirements

*   Python 3.x
*   NumPy
*   SciPy (likely used for linear algebra in flow solver)
*   Matplotlib (for plotting in `abm_ec_simulation_v2.py`)
*   JSON (standard library, for output in `abm_different_seed_loss_simulation.py`)

## Installation

1.  Clone this repository:
    ```bash
    git clone <your-repo-url>
    cd <your-repo-directory>
    ```
2.  It's recommended to use a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```
3.  Install the required packages. You can create a `requirements.txt` file with the following content:
    ```
    numpy
    scipy
    matplotlib
    ```
    Then install using pip:
    ```bash
    pip install -r requirements.txt
    ```
4.  **Crucially:** Create the `random_seed_list.py` file in the same directory. It should define a list variable named `random_seeds`. For example:
    ```python
    # random_seed_list.py
    random_seeds = list(range(1, 101)) # Creates seeds 1 through 100
    ```

## Usage

### Running a Single Simulation

To run a single simulation instance and potentially visualize the network:

1.  Modify parameters within `abm_ec_simulation_v2.py` as needed:
    *   `Nt`: Number of timesteps.
    *   `num_cell`: Initial number of cells per segment.
    *   `branch_rule`: Set to 1, 3, or 5 for the desired bifurcation rule.
    *   `branch_alpha`: Set the alpha value (relevant only if `branch_rule=5`).
    *   `plot_network_flag`: Set to `True` to generate plots during the simulation.
2.  Run the script:
    ```bash
    python abm_ec_simulation_v2.py
    ```

### Running Multiple Simulations / Parameter Sweeps

To run multiple simulations for statistical analysis (e.g., testing stability across different seeds or alpha values):

1.  Modify parameters within `abm_different_seed_loss_simulation.py`:
    *   Set the desired `branch_rule` (1, 3, or 5).
    *   Set the range of `branch_alpha` values to test (e.g., `branch_alpha_list = np.linspace(0, 1, 11)`). Note: Alpha is only used if `branch_rule=5`.
    *   Ensure `random_seed_list.py` contains the desired seeds. The script will iterate through these seeds for each parameter combination.
    *   Adjust `Nt` and `num_cell` if needed within the `run_simulation` function calls.
2.  Run the script:
    ```bash
    python abm_different_seed_loss_simulation.py
    ```

## Output

*   **Single Simulation (`abm_ec_simulation_v2.py`):** If `plot_network_flag=True`, Matplotlib plots showing the network state may be displayed or saved. Console output may show simulation progress.
*   **Multiple Simulations (`abm_different_seed_loss_simulation.py`):** The script generates JSON files in an `output` directory (it creates the directory if it doesn't exist). Each JSON file typically stores time-series data (like cell count, diameter, pressure) for one complete simulation run (specific seed and parameter set). These JSON files need to be post-processed using separate analysis scripts (not included) to calculate metrics like bifurcation stability percentages.


