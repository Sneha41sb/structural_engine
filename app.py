import streamlit as st
import numpy as np
import plotly.graph_objects as go
import ctypes
import os

# 1. UI Page & Platform Configurations
st.set_page_config(layout="wide")
st.title("Next-Gen Unified Lifecycle Engineering Engine")
st.caption("Ecosystem Dashboard: SOLIDWORKS Parametric Geometry, ANSYS Stress Simulation, and Site Logistics")

# 2. Dynamic Memory Bridge (C++ Core Engine Loader)
lib_path = os.path.abspath("libengine.so")
try:
    cpp_engine = ctypes.CDLL(lib_path)
    cpp_engine.simulate_and_optimize_core.argtypes = [ctypes.c_int, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double]
    cpp_engine.simulate_and_optimize_core.restype = ctypes.c_double
    cpp_is_ready = True
except Exception as e:
    cpp_is_ready = False

# 3. Sidebar Multi-Software Interaction Panels
st.sidebar.header("1. SOLIDWORKS Geometric Inputs")
num_floors = st.sidebar.slider("Number of Floors (Feature Tree Count)", min_value=1, max_value=10, value=5)
floor_height = st.sidebar.slider("Floor Height Dimension (m)", min_value=3.0, max_value=5.0, value=3.5)
bay_width = st.sidebar.slider("Bay Width Dimension (m)", min_value=4.0, max_value=8.0, value=6.0)

st.sidebar.header("2. ANSYS Mesh & Load Settings")
wind_force = st.sidebar.slider("Lateral Boundary Force (kN)", min_value=10, max_value=200, value=75)
drift_limit = st.sidebar.slider("Max Permissible Drift (mm)", min_value=5.0, max_value=25.0, value=12.0)
yield_strength = st.sidebar.slider("Material Yield Limit (kN/m²)", min_value=15000, max_value=40000, value=25000, step=1000)

st.sidebar.header("3. Field Logistics Constraints")
machinery_class = st.sidebar.selectbox(
    "Active Heavy Asset Weight Class",
    ["Utility Weight Asset (20-Ton Class)", "Heavy Duty Rig (50-Ton Class)", "High Capacity Transport (75-Ton Class)"]
)
dynamic_mode = st.sidebar.checkbox("Account for Dynamic Lifting Surcharge (Impact Factor 1.3x)", value=True)
selected_soil = st.sidebar.selectbox(
    "Site Terrain Stratum Profile",
    ["Loose Granular Strata", "Cohesive Clay Profile", "Indurated Bedrock"]
)

# 4. Standard Industrial Infrastructure Databases
machinery_db = {
    "Utility Weight Asset (20-Ton Class)": {"static_weight": 220.0, "area": 3.8},
    "Heavy Duty Rig (50-Ton Class)": {"static_weight": 490.0, "area": 5.2},
    "High Capacity Transport (75-Ton Class)": {"static_weight": 740.0, "area": 4.1}
}

soil_db = {
    "Loose Granular Strata": {"friction_angle": 30, "multiplier": 1.5, "bearing_capacity": 160.0},
    "Cohesive Clay Profile": {"friction_angle": 22, "multiplier": 1.2, "bearing_capacity": 240.0},
    "Indurated Bedrock": {"friction_angle": 45, "multiplier": 0.4, "bearing_capacity": 1200.0}
}

# 5. Integrated Ecosystem Math Pipeline Execution
if cpp_is_ready:
    # Pass input streams directly down to the high-speed compiled C++ optimization solver kernel
    optimized_area = cpp_engine.simulate_and_optimize_core(
        num_floors, floor_height, bay_width, float(wind_force), float(drift_limit), float(yield_strength)
    )
    
    # Process C++ output into driving dimensions for SOLIDWORKS design tables
    optimized_thickness = np.sqrt(optimized_area)
    
    # Calculate geometric volumes (Baseline vs Optimized)
    total_skeleton_length = (num_floors * 2 * floor_height) + (num_floors * bay_width)
    baseline_volume = total_skeleton_length * 0.25
    optimized_volume = total_skeleton_length * optimized_area
    volume_saved = baseline_volume - optimized_volume
    percentage_saved = (volume_saved / baseline_volume) * 100
    
    # SYSTEM INTERACTION BRIDGE: Structural mass feeds foundation dead load pressure rules
    building_pressure = (optimized_volume * 24.0) / (bay_width * 2.0)
    
    # Process logistics machine track footprint pressures
    asset = machinery_db[machinery_class]
    total_weight = asset["static_weight"] * (1.3 if dynamic_mode else 1.0)
    machinery_pressure = total_weight / asset["area"]
    
    # Combine forces for global geotechnical structural evaluation
    total_system_pressure = building_pressure + machinery_pressure
    soil = soil_db[selected_soil]
    
    phi_rad = np.radians(soil["friction_angle"])
    standoff_distance = 4.0 * np.tan(np.pi/4.0 - phi_rad/2.0) * soil["multiplier"]

    # FINANCIAL AND CARBON LIFE-CYCLE ESTIMATOR METHODOLOGIES
    concrete_unit_cost = 120.0  # Assumed standard global market unit cost per cubic meter ($/m³)
    carbon_intensity_factor = 320.0  # Embodied carbon footprint coefficient per cubic meter (kg CO₂e/m³)
    
    financial_savings = volume_saved * concrete_unit_cost
    carbon_mass_saved = volume_saved * carbon_intensity_factor

    # 6. Interactive Visual Dashboard Render
    col_vis, col_sim = st.columns([2, 1])
    
    with col_vis:
        st.subheader("Multi-Variable Topological Analysis")
        fig = go.Figure()
        
        # Draw architectural floor interval lines
        for f in range(num_floors + 1):
            z = f * floor_height
            fig.add_trace(go.Scatter(x=[0, bay_width], y=[z, z], mode='lines', line=dict(color='lightgray', width=1)))
            
        # Plot columns dynamically scaled by the native C++ optimization loop outputs
        lw = max(1, int(optimized_area * 60))
        fig.add_trace(go.Scatter(x=[0, 0], y=[0, num_floors*floor_height], mode='lines', line=dict(color='darkblue', width=lw), name="SOLIDWORKS Extrusion Profile"))
        fig.add_trace(go.Scatter(x=[bay_width, bay_width], y=[0, num_floors*floor_height], mode='lines', line=dict(color='darkblue', width=lw)))
        
        # Draw the open foundation safety clearance zone lines
        fig.add_trace(go.Scatter(x=[-standoff_distance, 0, 0], y=[0, 0, -4.0], mode='lines+markers', line=dict(color='crimson', width=3, dash='dot'), name="Exclusion Boundary"))
        
        fig.update_layout(xaxis_title='Site Coordinates (meters)', yaxis_title='Elevation / Foundation Pit Depth (meters)', height=440, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    with col_sim:
        st.subheader("Unified Multi-Software Validation Report")
        
        # SOLIDWORKS Integration UI Block
        st.markdown("**SOLIDWORKS Feature Driver Geometry**")
        st.caption(f"Driven Table Parameter: Square Column Section = **{optimized_thickness:.3f}m x {optimized_thickness:.3f}m**")
        
        # ANSYS Integration UI Block
        st.markdown("**ANSYS Finite Element Mesh Check**")
        if optimized_area == 0.25:
            st.warning("SIMULATION LOCK: Stress values reached material yield limits. Geometry locked at safety maximum boundary.")
        else:
            st.success("FEA VERIFICATION: Internal stress configurations stay safely within structural elastic limits.")
            
        # Logistics Integration UI Block
        st.markdown("**Combined Field Logistics Integration**")
        st.metric("Total Combined Subgrade Load", f"{total_system_pressure:.1f} kN/m²", delta=f"Soil Limit: {soil['bearing_capacity']} kN/m²", delta_color="inverse")
        
        if total_system_pressure > soil["bearing_capacity"]:
            st.error("OPERATIONS CRITICAL: Combined building mass and vehicle lifting surcharge exceed soil bearing capacity.")
        else:
            st.success("OPERATION SECURE: Terrain stability coefficients fully compliant.")

    # NEW ADVANCED ACCORDION PANEL: LIFE-CYCLE SUSTAINABILITY AND BUSINESS ANALYTICS
    st.markdown("---")
    st.subheader("Generative Value Engineering & Sustainability Analytics")
    
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Optimized Section Area", f"{optimized_area:.4f} m²", help="The minimized thickness required to withstand environmental wind loads calculated inside C++ machine code.")
    m2.metric("Total Material Optimized", f"{optimized_volume:.1f} m³", delta=f"-{percentage_saved:.1f}% Reduction")
    m3.metric("Project CapEx Saved", f"${financial_savings:,.2f}", delta="Cost Reduced", delta_color="normal")
    m4.metric("Embodied Carbon Offset", f"{carbon_mass_saved:.1f} kg CO₂e", delta="Emissions Cut", delta_color="normal")

    # Native Data Exporters Configuration Deck
    st.markdown("---")
    st.subheader("Native File Interoperability Data Exporters")
    exp1, exp2 = st.columns(2)
    
    with exp1:
        csv_data = f"Configuration Name,Column_Width,Column_Thickness,Bay_Width,Story_Height\n"
        csv_data += f"Optimized_Design_State,{optimized_thickness:.4f},{optimized_thickness:.4f},{bay_width:.2f},{floor_height:.2f}\n"
        st.download_button(
            label="Export SOLIDWORKS Design Table (.CSV)",
            data=csv_data,
            file_name="solidworks_design_table.csv",
            mime="text/csv"
        )
        
    with exp2:
        apdl_script = "/PREP7\nET,1,LINK180\nMP,EX,1,2.0E7\n"
        node_id = 1
        for f in range(num_floors + 1):
            z_coord = f * floor_height
            apdl_script += f"N,{node_id},0.0,0.0,{z_coord:.2f}\n"
            apdl_script += f"N,{node_id+1},{bay_width:.2f},0.0,{z_coord:.2f}\n"
            node_id += 2
        for f in range(num_floors):
            base_node = f * 2 + 1
            apdl_script += f"E,{base_node},{base_node+2}\n"
            apdl_script += f"E,{base_node+1},{base_node+3}\n"
            apdl_script += f"E,{base_node+2},{base_node+3}\n"
        apdl_script += "D,1,ALL,0\nD,2,ALL,0\n"
        top_left_node = num_floors * 2 + 1
        apdl_script += f"F,{top_left_node},FX,{wind_force:.2f}\n/SOLU\nSOLVE\n"
        st.download_button(
            label="Export ANSYS APDL Simulation Deck (.DAT)",
            data=apdl_script,
            file_name="ansys_simulation_deck.dat",
            mime="text/plain"
        )
else:
    st.error("High-speed C++ calculation library engine (`libengine.so`) could not be resolved or found.")