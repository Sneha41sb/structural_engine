#include <cmath>

extern "C" {

    // Advanced Core Solver mapping CAD feature limits and FEA stress evaluation metrics
    double simulate_and_optimize_core(int floors, double height, double width, double wind_load, double structural_safety_limit, double material_yield_strength) {
        
        double current_area = 0.25; // Default starting cross-section area (m²)
        double E = 2.0e7;           // Young's Modulus of structural concrete (kN/m²)
        
        // Generative Optimization Loop: Runs at native machine speed
        for (int i = 0; i < 100; i++) {
            double total_height = floors * height;
            double Moment_of_Inertia = (current_area * current_area) / 12.0;
            
            // 1. FEA Structural Simulation (ANSYS Principle)
            double total_height_cubed = total_height * total_height * total_height;
            double structural_drift = (wind_load * total_height_cubed) / (3.0 * E * Moment_of_Inertia);
            double drift_mm = structural_drift * 1000.0;
            
            // Calculate Max Internal Stress (Sigma = My / I)
            double max_bending_moment = wind_load * total_height; 
            double half_thickness = std::sqrt(current_area) / 2.0; 
            double calculated_stress = (max_bending_moment * half_thickness) / Moment_of_Inertia;
            
            // 2. Multi-Software Constraint Verification Check
            // If the structure bends too much OR exceeds material yield limits, reject the trim step
            if (drift_mm > structural_safety_limit || calculated_stress > material_yield_strength) {
                current_area += 0.005; // Revert to last safe geometric boundary profile
                break;
            }
            
            current_area -= 0.005; // Shave material area (CAD Optimization Action)
            
            if (current_area < 0.01) {
                current_area = 0.01;
                break;
            }
        }
        return current_area; // Return optimized parameter back to the web frontend
    }
}