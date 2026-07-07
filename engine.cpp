#include <cmath>

// extern "C" 
extern "C" {

    double simulate_and_optimize_core(int floors, double height, double width, double wind_load, double structural_safety_limit) {
        double current_area = 0.25; // element base starting size (m^2)
        double E = 2.0e7;           // Young's modulus of material 
        
        for (int i = 0; i < 100; i++) {
            double total_height = floors * height;
            double Moment_of_Inertia = (current_area * current_area) / 12.0;
            double total_height_cubed = total_height * total_height * total_height;
            double structural_drift = (wind_load * total_height_cubed) / (3.0 * E * Moment_of_Inertia);
            
            double drift_mm = structural_drift * 1000.0;
    
            if (drift_mm > structural_safety_limit) {
                current_area += 0.005;
                break;
            }
            current_area -= 0.005;
            //prevent the element from disappearing
            if (current_area < 0.01) {
                current_area = 0.01;
                break;
            }
        }
        return current_area;
    }
}