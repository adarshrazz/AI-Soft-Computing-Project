"""Plots for membership functions and the irrigation response surface."""
import numpy as np
import matplotlib.pyplot as plt
from membership import SOIL_MOISTURE_SETS, TEMPERATURE_SETS, triangular_membership
from sugeno import calculate_irrigation

def membership_figure():
    fig, axes = plt.subplots(1, 2, figsize=(11, 4))
    soil_x = np.linspace(0, 100, 401)
    for name, params in SOIL_MOISTURE_SETS.items():
        axes[0].plot(soil_x, [triangular_membership(x, *params) for x in soil_x], label=name, linewidth=2)
    axes[0].set_title("Soil moisture membership functions")
    axes[0].set_xlabel("Soil moisture (%)")
    axes[0].set_ylabel("Membership degree")
    axes[0].set_ylim(-0.03, 1.05)
    axes[0].grid(alpha=0.25)
    axes[0].legend()

    temp_x = np.linspace(0, 50, 401)
    for name, params in TEMPERATURE_SETS.items():
        axes[1].plot(temp_x, [triangular_membership(x, *params) for x in temp_x], label=name, linewidth=2)
    axes[1].set_title("Temperature membership functions")
    axes[1].set_xlabel("Temperature (°C)")
    axes[1].set_ylabel("Membership degree")
    axes[1].set_ylim(-0.03, 1.05)
    axes[1].grid(alpha=0.25)
    axes[1].legend()
    fig.tight_layout()
    return fig

def response_surface_figure():
    soil_values = np.linspace(0, 100, 41)
    temp_values = np.linspace(0, 50, 31)
    z = np.zeros((len(temp_values), len(soil_values)))
    for yi, temp in enumerate(temp_values):
        for xi, soil in enumerate(soil_values):
            z[yi, xi] = calculate_irrigation(float(soil), float(temp))["duration_minutes"]
    fig, ax = plt.subplots(figsize=(8, 4.5))
    mesh = ax.contourf(soil_values, temp_values, z, levels=15)
    fig.colorbar(mesh, ax=ax, label="Irrigation duration (minutes)")
    ax.set_title("Sugeno model response surface")
    ax.set_xlabel("Soil moisture (%)")
    ax.set_ylabel("Temperature (°C)")
    fig.tight_layout()
    return fig
