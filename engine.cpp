#include <cmath>

// extern "C" makes the compiled symbols plainly visible to Python's ctypes interface
extern "C" {

    double simulate_and_optimize_core(int floors, double height, double width, double wind_load, double structural_safety_limit) {
        double current_area = 0.25; // Base starting cross-sectional area (m²)
        double E = 2.0e7;           // Young's Modulus of standard structural concrete (kN/m²)
        
        // Generative Optimization Loop: Iteratively trims material sizes at machine speeds
        for (int i = 0; i < 100; i++) {
            double total_height = floors * height;
            double Moment_of_Inertia = (current_area * current_area) / 12.0;
            
            // High-speed manual cubing calculation loop (Fast replacement for std::pow)
            double total_height_cubed = total_height * total_height * total_height;
            double structural_drift = (wind_load * total_height_cubed) / (3.0 * E * Moment_of_Inertia);
            
            double drift_mm = structural_drift * 1000.0;
            
            // Constraint Boundary Check: If the building sways past limits, step back to last safe size and exit
            if (drift_mm > structural_safety_limit) {
                current_area += 0.005;
                break;
            }
            
            // Value Engineering Action: Safely reduce cross-sectional thickness
            current_area -= 0.005;
            
            // Safety guardrail to prevent physical elements from disappearing to zero
            if (current_area < 0.01) {
                current_area = 0.01;
                break;
            }
        }
        return current_area; // Returns optimized structural dimensions down to Python
    }
}