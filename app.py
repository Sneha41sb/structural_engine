import streamlit as st
import numpy as np
import plotly.graph_objects as go
import ctypes
import os

# 1. Page Configuration
st.set_page_config(layout="wide")
st.title("Next-Gen Unified Lifecycle Engineering Engine")
st.caption("A Fully Integrated Platform Combining Parametric CAD Design, C++ Optimization Math, and Geotechnical Logistics")

# 2. Dynamic C++ Shared Library Binding Bridge
lib_path = os.path.abspath("libengine.so")
try:
    cpp_engine = ctypes.CDLL(lib_path)
    cpp_engine.simulate_and_optimize_core.argtypes = [ctypes.c_int, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double]
    cpp_engine.simulate_and_optimize_core.restype = ctypes.c_double
    cpp_is_ready = True
except Exception as e:
    cpp_is_ready = False

# 3. Sidebar Configuration Layout
st.sidebar.header("1. Structural Design Parameters")
num_floors = st.sidebar.slider("Number of Floors", min_value=1, max_value=10, value=5)
floor_height = st.sidebar.slider("Floor Height (m)", min_value=3.0, max_value=5.0, value=3.5)
bay_width = st.sidebar.slider("Bay Width (m)", min_value=4.0, max_value=8.0, value=6.0)
wind_force = st.sidebar.slider("Lateral Wind Forces (kN)", min_value=10, max_value=200, value=60)
safety_threshold = st.sidebar.slider("Max Allowed Drift Limit (mm)", min_value=5.0, max_value=25.0, value=12.0)

st.sidebar.header("2. Construction Site Variables")
selected_machine = st.sidebar.selectbox(
    "Active Logistics Machinery Profile",
    ["Utility Class Excavator (20-Ton)", "Heavy Duty Excavator (50-Ton)", "High Capacity Hauler (75-Ton)"]
)
selected_soil = st.sidebar.selectbox(
    "Site Foundation Subgrade Type",
    ["Loose Granular Subgrade (Low Bearing Capacity)", "Cohesive Clay Layer (Medium Bearing Capacity)", "Solid Bedrock (High Bearing Capacity)"]
)

# 4. Standard Technical Infrastructure Databases
machinery_database = {
    "Utility Class Excavator (20-Ton)": {"weight_kn": 220.0, "track_area_m2": 3.8, "desc": "Standard earthmoving utility."},
    "Heavy Duty Excavator (50-Ton)": {"weight_kn": 490.0, "track_area_m2": 5.2, "desc": "Deep foundation infrastructure deployment."},
    "High Capacity Hauler (75-Ton)": {"weight_kn": 740.0, "track_area_m2": 4.1, "desc": "Heavy transport (Fully loaded weight specification)."}
}

soil_database = {
    "Loose Granular Subgrade (Low Bearing Capacity)": {"friction_angle": 30, "safe_multiplier": 1.5, "max_bearing_capacity": 150.0},
    "Cohesive Clay Layer (Medium Bearing Capacity)": {"friction_angle": 22, "safe_multiplier": 1.2, "max_bearing_capacity": 250.0},
    "Solid Bedrock (High Bearing Capacity)": {"friction_angle": 45, "safe_multiplier": 0.4, "max_bearing_capacity": 1000.0}
}

# 5. Core Systems Integration Execution
if cpp_is_ready:
    # SYSTEM 1 & 2: Structural Inputs flow into the high-speed C++ optimization solver kernel
    optimized_area = cpp_engine.simulate_and_optimize_core(
        num_floors, floor_height, bay_width, float(wind_force), float(safety_threshold)
    )
    
    # Calculate structural geometry mass properties
    initial_volume = (num_floors * 2 * floor_height + num_floors * bay_width) * 0.25
    optimized_volume = (num_floors * 2 * floor_height + num_floors * bay_width) * optimized_area
    material_saved = ((initial_volume - optimized_volume) / initial_volume) * 100
    
    # SYSTEM 3: Structural weight flows directly into the Geotechnical Surcharge Logistics Module
    concrete_density = 24.0  # Standard density weight of structural concrete (kN/m³)
    building_dead_load_weight = optimized_volume * concrete_density
    building_pressure_on_soil = building_dead_load_weight / (bay_width * 2.0) # distributed pressure
    
    # Process machinery ground track loads
    machine = machinery_database[selected_machine]
    soil = soil_database[selected_soil]
    machinery_track_pressure = machine["weight_kn"] / machine["track_area_m2"]
    
    # Calculate Total Combined Foundation System Pressure
    total_combined_site_pressure = building_pressure_on_soil + machinery_track_pressure
    
    # Compute critical excavation pit standoff boundaries using Rankine soil mechanics
    foundation_depth = 4.0  
    phi_rad = np.radians(soil["friction_angle"])
    critical_distance = foundation_depth * np.tan(np.pi/4.0 - phi_rad/2.0) * soil["safe_multiplier"]

    # 6. User Interface Rendering
    col_left, col_right = st.columns([2, 1])
    
    with col_left:
        st.subheader("Unified System Topology View")
        fig = go.Figure()
        
        # Plot building blueprint grids
        for f in range(num_floors + 1):
            z = f * floor_height
            fig.add_trace(go.Scatter(x=[0, bay_width], y=[z, z], mode='lines', line=dict(color='lightgray', width=2)))
            
        line_width_pixel = max(1, int(optimized_area * 60))
        fig.add_trace(go.Scatter(x=[0, 0], y=[0, num_floors*floor_height], mode='lines', line=dict(color='blue', width=line_width_pixel), name="Optimized Frame"))
        fig.add_trace(go.Scatter(x=[bay_width, bay_width], y=[0, num_floors*floor_height], mode='lines', line=dict(color='blue', width=line_width_pixel)))
        
        # Plot excavation slip lines
        fig.add_trace(go.Scatter(x=[-critical_distance, 0, 0], y=[0, 0, -foundation_depth], mode='lines+markers', line=dict(color='red', width=3, dash='dash'), name="Exclusion Zone Boundary"))
        
        fig.update_layout(xaxis_title='Site Coordinates (meters)', yaxis_title='Elevation / Excavation Depth (meters)', height=450, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    with col_right:
        st.subheader(" Unified Safety Dashboard")
        
        st.metric("Structure Dead Load Pressure", f"{building_pressure_on_soil:.1f} kN/m²")
        st.metric("Machinery Footprint Pressure", f"{machinery_track_pressure:.1f} kN/m²")
        st.markdown("---")
        st.metric("Total Combined System Load", f"{total_combined_site_pressure:.1f} kN/m²", delta=f"Soil Limit: {soil['max_bearing_capacity']} kN/m²", delta_color="inverse")
        
        # Multi-variable structural-geotechnical validation logic
        if total_combined_site_pressure > soil["max_bearing_capacity"]:
            st.error("SYSTEM CRITICAL SHUTDOWN: Combined building mass and machinery surcharge loads exceed soil bearing capacity thresholds. Structural settlement or failure imminent.")
        else:
            st.success("TOTAL DESIGN ECOSYSTEM SECURE: Integrated structural and site variables are fully stable.")

    # Bottom Core Analytics Ribbon
    st.markdown("---")
    m1, m2, m3 = st.columns(3)
    m1.metric("C++ Optimized Cross-Section", f"{optimized_area:.4f} m²")
    m2.metric("Total Design Core Material Volume", f"{optimized_volume:.2f} m³")
    m3.metric("Embodied Carbon Material Savings", f"{material_saved:.1f} %", delta=f"-{material_saved:.1f}% Savings")
else:
    st.error("High-speed computational library core file (`libengine.so`) could not be resolved or found.")