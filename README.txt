This project is a work-in-progress simulation of the Pratt & Whitney F119 turbofan engine, used on the F-22 Raptor.

The core classes and thermodynamic equations have been verified (based on Anderson’s Modern Compressible Flow and other references) and the engine flowpath (inlet → fan → bypass → HPC → combustor → turbines → mixer → afterburner → nozzle → exhaust) is ~90% complete.

However, the current implementation does not yet produce realistic thrust results due to how the inlet mass flow and nozzle expansion are being linked. The individual component physics are correct, but the final coupling still needs refinement.

Due to time constraints and shifting priorities, I’m pausing development here. Future work will focus on:

- Iteratively solving for nozzle exit Mach and area (variable geometry),

- Validating mass flow to match real F119 performance (~232 kN afterburning thrust per engine),

- Smoothing thrust and TSFC trends across the Mach range.

For now, the repository serves as a reference for the completed engine component models and a near-finished integrated cycle. I’ll return to finalize and calibrate the simulation at a later date.