import numpy as np
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

# Set global style for professional appearance
plt.rcParams.update({
    "font.family": "serif",
    "axes.titlesize": 14,
    "axes.labelsize": 12,
    "xtick.labelsize": 10,
    "ytick.labelsize": 10,
    "legend.fontsize": 10
})

# Simulate dataset
np.random.seed(42)
n_samples = 1000
n_features = 50

X = np.random.rand(n_samples, n_features)
y = np.sin(2 * np.pi * X[:, 0]) + np.log(X[:, 1] + 1) + 0.5 * np.random.randn(n_samples)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Experiment 1: MSE vs Leaf Nodes per Tree
leaf_nodes = np.linspace(2, 500, 20, dtype=int)
ensemble_sizes_fixed = [1, 5, 10, 50]
dt_test_errors = {ens: [] for ens in ensemble_sizes_fixed}

for leaves in leaf_nodes:
    for ens in ensemble_sizes_fixed:
        rf = RandomForestRegressor(n_estimators=ens, max_leaf_nodes=leaves, random_state=42)
        rf.fit(X_train, y_train)
        dt_test_errors[ens].append(mean_squared_error(y_test, rf.predict(X_test)))

# Experiment 2: MSE vs Ensemble Size
ensemble_sizes = np.linspace(1, 100, 15, dtype=int)
tree_depths_fixed = [20, 50, 100, 500]
rf_test_errors = {depth: [] for depth in tree_depths_fixed}

for ens in ensemble_sizes:
    for depth in tree_depths_fixed:
        rf = RandomForestRegressor(n_estimators=ens, max_leaf_nodes=depth, random_state=42)
        rf.fit(X_train, y_train)
        rf_test_errors[depth].append(mean_squared_error(y_test, rf.predict(X_test)))

# Transition experiment
composite_leaf_nodes = np.linspace(2, n_samples, 30, dtype=int)
composite_ensemble_sizes = np.linspace(1, 100, 15, dtype=int)
composite_test_errors = []

for leaves in composite_leaf_nodes:
    tree = DecisionTreeRegressor(max_leaf_nodes=leaves, random_state=42)
    tree.fit(X_train, y_train)
    composite_test_errors.append(mean_squared_error(y_test, tree.predict(X_test)))

for ens in composite_ensemble_sizes:
    forest = RandomForestRegressor(n_estimators=ens, max_leaf_nodes=n_samples, random_state=42)
    forest.fit(X_train, y_train)
    composite_test_errors.append(mean_squared_error(y_test, forest.predict(X_test)))

interpolation_idx = np.argmax(composite_test_errors)

# Create multipanel figure
fig, axes = plt.subplots(1, 3, figsize=(18, 5), dpi=300, sharey=True, gridspec_kw={'width_ratios': [1, 1, 1.2]})

# Panel 1: MSE vs Leaf Nodes
colors = ["#4C72B0", "#55A868", "#C44E52", "#8172B2"]
for i, ens in enumerate(ensemble_sizes_fixed):
    axes[0].plot(leaf_nodes, dt_test_errors[ens], color=colors[i], linewidth=2, label=f"Trees={ens}")
axes[0].set_title("Error by Leaf Nodes (Fixed Trees)")
axes[0].set_xlabel("Number of Leaf Nodes")
axes[0].set_ylabel("MSE")
axes[0].legend()

# Panel 2: MSE vs Ensemble Size
colors = ["#DD8452", "#55A868", "#C44E52", "#8172B2"]
for i, depth in enumerate(tree_depths_fixed):
    axes[1].plot(ensemble_sizes, rf_test_errors[depth], color=colors[i], linewidth=2, label=f"Depth={depth}")
axes[1].set_title("Error by Ensemble Size (Fixed Depth)")
axes[1].set_xlabel("Number of Trees")
axes[1].legend()
axes[1].set_yticklabels([])  # Remove y-ticks for middle plot

# Panel 3: Continuous Test Error Line
composite_x_axis = [f"L{l}" for l in composite_leaf_nodes] + [f"E{e}" for e in composite_ensemble_sizes]
axes[2].plot(range(len(composite_x_axis)), composite_test_errors, color="black", linewidth=2, label="Test Error")
axes[2].axvline(interpolation_idx, color='black', linestyle='dashed', linewidth=2, label="Interpolation Threshold")
axes[2].set_title("Double Descent in Trees")
axes[2].set_xlabel("Boosting Rounds → Ensembling")
axes[2].set_xticks(range(0, len(composite_x_axis), max(len(composite_x_axis) // 6, 1)))
axes[2].set_xticklabels([composite_x_axis[i] for i in range(0, len(composite_x_axis), max(len(composite_x_axis) // 6, 1))], rotation=20, ha="right", fontsize=10)
axes[2].legend()
axes[2].set_yticklabels([])  # Remove y-ticks for right plot

plt.tight_layout()
plt.show()
