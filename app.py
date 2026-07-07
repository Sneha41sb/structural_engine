import streamlit as st
import numpy as np
import plotly.graph_objects as go
import ctypes
import os

# 1. Page Configuration
st.set_page_config(layout="wide")
st.title("Hybrid C++ & Python Generative Engineering Engine")
st.caption("Core Physics Math processing executing inside native compiled C++ shared library files")

# 2. Bind and Load the C++ Compiled Binary Engine
# This lets Python pass data straight down to your C++ functions in RAM
lib_path = os.path.abspath("libengine.so")
try:
    cpp_engine = ctypes.CDLL(lib_path)
    # Define the input data types and return types for the C++ function
    cpp_engine.simulate_and_optimize_core.argtypes = [ctypes.c_int, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double]
    cpp_engine.simulate_and_optimize_core.restype = ctypes.c_double
    cpp_is_ready = True
except Exception as e:
    cpp_is_ready = False
    st.error(f"Could not load C++ Shared Library: {e}")

# 3. Sidebar Configuration Layout
st.sidebar.header("Structural Parameters")
num_floors = st.sidebar.slider("Number of Floors", min_value=1, max_value=10, value=5)
floor_height = st.sidebar.slider("Floor Height (m)", min_value=3.0, max_value=5.0, value=3.5)
bay_width = st.sidebar.slider("Bay Width (m)", min_value=4.0, max_value=8.0, value=6.0)
wind_force = st.sidebar.slider("Lateral Wind Forces (kN)", min_value=10, max_value=200, value=60)
safety_threshold = st.sidebar.slider("Max Allowed Drift Limit (mm)", min_value=5.0, max_value=25.0, value=12.0)

# 4. Running the C++ Loop Engine Execution
if cpp_is_ready:
    st.subheader("Real-time C++ Loop Engine Calculations")
    
    # Call the C++ engine function directly!
    optimized_area = cpp_engine.simulate_and_optimize_core(
        num_floors, floor_height, bay_width, float(wind_force), float(safety_threshold)
    )
    
    # Showcase data results calculated inside C++
    initial_volume = (num_floors * 2 * floor_height + num_floors * bay_width) * 0.25
    optimized_volume = (num_floors * 2 * floor_height + num_floors * bay_width) * optimized_area
    material_saved = ((initial_volume - optimized_volume) / initial_volume) * 100
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Optimized Cross-Section Area", f"{optimized_area:.4f} m²")
    col2.metric("Final C++ Calculated Volume", f"{optimized_volume:.2f} m³")
    col3.metric("Total Material Weight Saved", f"{material_saved:.1f} %", delta=f"{material_saved:.1f}% Reduced")
    
    # 5. Fast Render 3D Interface View
    fig = go.Figure()
    # Simple geometry visualization mapping out structural nodes
    for f in range(num_floors + 1):
        z = f * floor_height
        fig.add_trace(go.Scatter3d(x=[0, bay_width], y=[0, 0], z=[z, z], mode='lines+markers', line=dict(color='black', width=3)))
    fig.add_trace(go.Scatter3d(x=[0, 0], y=[0, 0], z=[0, num_floors*floor_height], mode='lines', line=dict(color='blue', width=int(optimized_area*50))))
    fig.add_trace(go.Scatter3d(x=[bay_width, bay_width], y=[0, 0], z=[0, num_floors*floor_height], mode='lines', line=dict(color='blue', width=int(optimized_area*50))))
    
    fig.update_layout(scene=dict(xaxis_title='X', yaxis_title='Y', zaxis_title='Z'), height=500, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)