import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from polarizer_fit import (
    fit_malus_law,
    malus_law,
    radians_to_degrees,
    get_crossed_angle,
    get_parallel_angle,
)

# sample data
# 0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160
# 0.75, 0.42, 0.34, 0.2, 0.24, 0.3, 0.68, 0.68, 0.87, 1.03, 1.3, 1.22, 1.33, 1.29, 0.97, 0.91, 0.84


def main():
    st.title("Data Plotter")

    # Get user input
    x_data = st.text_input(
        label="Enter angles in degrees (comma-separated):",
        value="0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160",
    )
    y_data = st.text_input(
        label="Enter intensity data (comma-separated):",
        value="0.75, 0.42, 0.34, 0.2, 0.24, 0.3, 0.68, 0.68, 0.87, 1.03, 1.3, 1.22, 1.33, 1.29, 0.97, 0.91, 0.84",
    )

    if not x_data or not y_data:
        st.warning("Please enter some data.")
        return

    if len(x_data.split(",")) != len(y_data.split(",")):
        st.warning(f"len(x) = {len(x_data.split(','))}")
        st.warning(f"len(y) = {len(y_data.split(','))}")
        st.warning("X and Y data must have the same number of elements.")
        return

    # Convert input to lists of floats
    x_values = [float(x.strip()) for x in x_data.split(",")]
    y_values = [float(y.strip()) for y in y_data.split(",")]
    x_values = np.array(x_values)  # Convert to numpy array
    y_values = np.array(y_values)

    length_condition = len(x_values) == len(y_values)
    none_condition = x_values is not None and y_values is not None
    active_conditions = length_condition and none_condition

    if st.button("Show Raw Data"):
        # Plot the data
        fig, ax = plt.subplots()
        ax.plot(x_values, y_values, "o-")
        ax.set_xlabel("angle (degrees)")  # Use set_xlabel instead of xlabel
        ax.set_ylabel("Intensity")  # Use set_ylabel instead of ylabel
        ax.set_title("show raw data")  # Use set_title instead of title
        ax.grid(True, alpha=0.5)

        st.pyplot(fig)

    if st.button("Fit Malus Law"):
        if active_conditions:
            popt, pcov = fit_malus_law(x_values, y_values)
            st.sidebar.write(f"I0_fit: {popt[0]:.2f}")
            phi_deg = radians_to_degrees(popt[1])
            st.sidebar.write(f"phi_fit: {phi_deg:.2f} degrees")
            st.sidebar.write(f"offset_fit: {popt[2]:.2f}")

            parallel_angle = get_parallel_angle(phi_deg)
            st.sidebar.write(
                f"parallel_angle: {parallel_angle:.2f}"
            )  # Display in sidebar
            crossed_angle = get_crossed_angle(phi_deg)
            st.sidebar.write(f"crossed_angle: {crossed_angle:.2f}")

            # Plot the data
            fig, ax = plt.subplots()
            ax.plot(x_values, y_values, "o--", label="raw data")
            y_fit = malus_law(x_values, *popt)
            ax.plot(x_values, y_fit, linestyle="-", label="fit")
            ax.set_xlabel("angle (degrees)")  # Use set_xlabel instead of xlabel
            ax.set_ylabel("Intensity")  # Use set_ylabel instead of ylabel
            ax.set_title("curve fit")  # Use set_title instead of title
            ax.legend()
            ax.grid(True, alpha=0.5)
            st.pyplot(fig)

        else:
            st.warning("Data in invalid format.")


if __name__ == "__main__":
    main()
