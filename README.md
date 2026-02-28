# 4D_Flow_MRI_corrrection

## **Overview**
This project simulates how spatial inaccuracies in MRI gradient hardware bias velocity measurements in Phase Contrast MRI (PC-MRI). It models the discrepancy between the nominal **VENC** set by the user and the effective **VENC** actually delivered by the hardware.
## **Modeling Assumptions**
Gradient Roll-off: We assume a physically reasonable 1D model where gradient strength weakens as a function of distance from the isocenter.  
This is modeled quadratically: $G_{eff}(x) = G_{nom} \cdot (1 + \alpha(x/L)^2)$ with $\alpha = -0.1$.  
Constant Flow: The simulation assumes a "true" constant velocity of $0.5 \text{ m/s}$ across the entire field of view.  
Phase Encoding: Velocity is encoded into phase ($\phi$) based on the local effective gradient.  
The scanner then back-calculates velocity using the incorrect (nominal) **VENC**.  

## **Correction Strategy**
The "Bonus" correction assumes the nonlinearity profile ($\alpha$) is known via phantom calibration.  
The measured velocity ($v_{meas}$) is corrected by dividing it by the local gradient deviation factor, successfully recovering the true velocity across all positions.  
File Included **pc_mri_simulation.py**: Python script containing the hardware model, signal simulation, and correction visualization.  
Python script uses two modules Matplotlib & NumPy
