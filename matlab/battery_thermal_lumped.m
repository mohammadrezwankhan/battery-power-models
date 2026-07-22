function temperature_c = battery_thermal_lumped(currents_a, dt_s, params, initial_c)
%BATTERY_THERMAL_LUMPED First-order battery thermal reference model.
%   C_th*dT/dt = I^2*R - hA*(T - T_ambient)

arguments
    currents_a (1,:) double
    dt_s (1,1) double {mustBePositive}
    params.resistance_ohm (1,1) double {mustBeNonnegative} = 0.003
    params.thermal_capacitance_j_per_k (1,1) double {mustBePositive} = 5000
    params.cooling_conductance_w_per_k (1,1) double {mustBePositive} = 4
    params.ambient_c (1,1) double = 25
    initial_c (1,1) double = params.ambient_c
end

temperature_c = zeros(1, numel(currents_a) + 1);
temperature_c(1) = initial_c;
decay = exp(-params.cooling_conductance_w_per_k * dt_s / params.thermal_capacitance_j_per_k);

for index = 1:numel(currents_a)
    heat_w = currents_a(index)^2 * params.resistance_ohm;
    steady_c = params.ambient_c + heat_w / params.cooling_conductance_w_per_k;
    temperature_c(index + 1) = steady_c + (temperature_c(index) - steady_c) * decay;
end
end
