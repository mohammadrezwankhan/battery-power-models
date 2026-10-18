function temperature_c = battery_thermal_lumped(currents_a, dt_s, params, initial_c)
%BATTERY_THERMAL_LUMPED First-order battery thermal reference model.
%   C_th*dT/dt = I^2*R - hA*(T - T_ambient)
%   PARAMS is an optional scalar struct; omitted fields use the defaults below.
%   INITIAL_C defaults to the configured ambient temperature.

validateattributes(currents_a, {'numeric'}, {'row', 'real', 'finite'});
validateattributes(dt_s, {'numeric'}, {'scalar', 'real', 'finite', 'positive'});
if nargin < 3
    params = struct();
end
validateattributes(params, {'struct'}, {'scalar'});
defaults = struct('resistance_ohm', 0.003, ...
    'thermal_capacitance_j_per_k', 5000, ...
    'cooling_conductance_w_per_k', 4, 'ambient_c', 25);
names = fieldnames(defaults);
for index = 1:numel(names)
    name = names{index};
    if ~isfield(params, name)
        params.(name) = defaults.(name);
    end
    validateattributes(params.(name), {'numeric'}, {'scalar', 'real', 'finite'});
    params.(name) = double(params.(name));
end
validateattributes(params.resistance_ohm, {'numeric'}, {'nonnegative'});
validateattributes(params.thermal_capacitance_j_per_k, {'numeric'}, {'positive'});
validateattributes(params.cooling_conductance_w_per_k, {'numeric'}, {'positive'});
if nargin < 4
    initial_c = params.ambient_c;
end
validateattributes(initial_c, {'numeric'}, {'scalar', 'real', 'finite'});
currents_a = double(currents_a);
dt_s = double(dt_s);
initial_c = double(initial_c);

temperature_c = zeros(1, numel(currents_a) + 1);
temperature_c(1) = initial_c;
decay = exp(-params.cooling_conductance_w_per_k * dt_s / params.thermal_capacitance_j_per_k);

for index = 1:numel(currents_a)
    heat_w = currents_a(index)^2 * params.resistance_ohm;
    steady_c = params.ambient_c + heat_w / params.cooling_conductance_w_per_k;
    temperature_c(index + 1) = steady_c + (temperature_c(index) - steady_c) * decay;
end
end
