import streamlit as st
import numpy as np
import plotly.graph_objects as go
import ctypes
import os

# 1. Page & Layout Configuration
st.set_page_config(layout="wide")
st.title("Next-Gen 3D Unified Lifecycle Engineering Engine")
st.caption("Advanced 3D Workspace Dashboard: SOLIDWORKS Parametric Geometry, ANSYS Stress Simulation, and Site Logistics")

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
    # Trigger native high-speed C++ optimization solver kernel
    optimized_area = cpp_engine.simulate_and_optimize_core(
        num_floors, floor_height, bay_width, float(wind_force), float(drift_limit), float(yield_strength)
    )
    
    optimized_thickness = np.sqrt(optimized_area)
    
    # Calculate volumetric properties
    total_skeleton_length = (num_floors * 4 * floor_height) + (num_floors * 4 * bay_width)
    baseline_volume = total_skeleton_length * 0.25
    optimized_volume = total_skeleton_length * optimized_area
    volume_saved = baseline_volume - optimized_volume
    percentage_saved = (volume_saved / baseline_volume) * 100
    
    # Structural mass pressure bridge
    building_pressure = (optimized_volume * 24.0) / (bay_width * bay_width)
    
    # Process logistics machine track pressures
    asset = machinery_db[machinery_class]
    total_weight = asset["static_weight"] * (1.3 if dynamic_mode else 1.0)
    machinery_pressure = total_weight / asset["area"]
    
    # Combined Geotechnical metrics
    total_system_pressure = building_pressure + machinery_pressure
    soil = soil_db[selected_soil]
    
    phi_rad = np.radians(soil["friction_angle"])
    standoff_distance = 4.0 * np.tan(np.pi/4.0 - phi_rad/2.0) * soil["multiplier"]

    concrete_unit_cost = 120.0  
    carbon_intensity_factor = 320.0  
    financial_savings = volume_saved * concrete_unit_cost
    carbon_mass_saved = volume_saved * carbon_intensity_factor

    # 6. Interactive Visual Dashboard Render (Upgraded to 3D)
    col_vis, col_sim = st.columns([2, 1])
    
    with col_vis:
        st.subheader("3D Interactive Topology Space")
        fig = go.Figure()
        
        # Line width mapping for 3D elements
        lw_3d = max(2, int(optimized_area * 50))
        
        # GENERATIVE 3D FRAME MODELING GRID LOOP (SOLIDWORKS & ANSYS WIREFRAME PARADIGM)
        corners = [(0, 0), (bay_width, 0), (bay_width, bay_width), (0, bay_width)]
        
        # Plot 4 Vertical 3D Column Members
        for cx, cy in corners:
            fig.add_trace(go.Scatter3d(
                x=[cx, cx], 
                y=[cy, cy], 
                z=[0, num_floors * floor_height],
                mode='lines', 
                line=dict(color='darkblue', width=lw_3d), 
                name="Column Element"
            ))
            
        # Plot Horizontal 3D Floor Diaphragm Beam Members
        for f in range(1, num_floors + 1):
            z_val = f * floor_height
            bx = [0, bay_width, bay_width, 0, 0]
            by = [0, 0, bay_width, bay_width, 0]
            bz = [z_val, z_val, z_val, z_val, z_val]
            fig.add_trace(go.Scatter3d(
                x=bx, 
                y=by, 
                z=bz,
                mode='lines', 
                line=dict(color='royalblue', width=max(1, lw_3d // 2)), 
                name="Beam Element"
            ))

        # GEOTECHNICAL SAFETY ZONE SURFACE MAPPING (3D CONTAINER ZONE)
        sx = [-standoff_distance, bay_width + standoff_distance, bay_width + standoff_distance, -standoff_distance, -standoff_distance]
        sy = [-standoff_distance, -standoff_distance, bay_width + standoff_distance, bay_width + standoff_distance, -standoff_distance]
        sz = [0, 0, 0, 0, 0]
        
        fig.add_trace(go.Scatter3d(
            x=sx, 
            y=sy, 
            z=sz,
            mode='lines', 
            line=dict(color='crimson', width=4, dash='dot'), 
            name="Exclusion Boundary"
        ))
        
        # Establish viewport camera configurations
        fig.update_layout(
            scene=dict(
                xaxis_title='X: Site Width (m)',
                yaxis_title='Y: Site Depth (m)',
                zaxis_title='Z: Elevation (m)',
                camera=dict(eye=dict(x=1.5, y=1.5, z=1.2))
            ),
            height=500,
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)

    with col_sim:
        st.subheader("Unified Multi-Software Validation Report")
        
        # SOLIDWORKS Integration UI Block
        st.markdown("**SOLIDWORKS Structural Feature Parameters**")
        st.caption(f"Driven Table Parameter: Square Column Section = {optimized_thickness:.3f}m x {optimized_thickness:.3f}m")
        
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

    # LIFE-CYCLE SUSTAINABILITY AND BUSINESS ANALYTICS PANEL
    st.markdown("---")
    st.subheader("Generative Value Engineering & Sustainability Analytics")
    
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Optimized Section Area", f"{optimized_area:.4f} m²")
    m2.metric("Total Material Optimized", f"{optimized_volume:.1f} m³", delta=f"-{percentage_saved:.1f}% Reduction")
    m3.metric("Project CapEx Saved", f"${financial_savings:,.2f}", delta="Cost Reduced")
    m4.metric("Embodied Carbon Offset", f"{carbon_mass_saved:.1f} kg CO₂e", delta="Emissions Cut")

    # Native Data Exporters Configuration Deck
    st.markdown("---")
    st.subheader("Native File Interoperability Data Exporters")
    exp1, exp2 = st.columns(2)
    
    with exp1:
        csv_data = f"Configuration Name,Column_Width,Column_Thickness,Bay_Width,Story_Height\n"
        csv_data += f"Optimized_Design_State,{optimized_thickness:.4f},{optimized_thickness:.4f},{bay_width:.2f},{floor_height:.2f}\n"
        st.download_button(label="Export SOLIDWORKS Design Table (.CSV)", data=csv_data, file_name="solidworks_design_table.csv", mime="text/csv")
        
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
        st.download_button(label="Export ANSYS APDL Simulation Deck (.DAT)", data=apdl_script, file_name="ansys_simulation_deck.dat", mime="text/plain")
else:
    st.close()
    st.error("High-speed C++ calculation library engine (libengine.so) could not be resolved or found.")