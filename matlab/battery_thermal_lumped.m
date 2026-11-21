function temperature_c = battery_thermal_lumped(currents_a, dt_s, params, initial_c)
%BATTERY_THERMAL_LUMPED First-order battery thermal reference model.
%   C_th*dT/dt = I^2*R - hA*(T - T_ambient)
%   PARAMS is an optional scalar struct; omitted fields use the defaults below.
%   INITIAL_C defaults to the configured ambient temperature.

validateattributes(currents_a, {'numeric'}, {'row', 'real', 'finite', 'nonempty'});
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
validateattributes(params.cooling_conductance_w_per_k, {'numeric'}, {'nonnegative'});
if nargin < 4
    initial_c = params.ambient_c;
end
validateattributes(initial_c, {'numeric'}, {'scalar', 'real', 'finite'});
currents_a = double(currents_a);
dt_s = double(dt_s);
initial_c = double(initial_c);

temperature_c = zeros(1, numel(currents_a) + 1);
temperature_c(1) = initial_c;
conductance = params.cooling_conductance_w_per_k;
capacitance = params.thermal_capacitance_j_per_k;
x = (conductance * dt_s) / capacitance;
if ~isfinite(x)
    x = (conductance / capacitance) * dt_s;
end
decay = exp(-x);

for index = 1:numel(currents_a)
    if currents_a(index) == 0 || params.resistance_ohm == 0
        heat_w = 0;
    else
        heat_w = currents_a(index)^2 * params.resistance_ohm;
        if ~isfinite(heat_w) || (heat_w == 0 && currents_a(index) ~= 0)
            heat_w = (currents_a(index) * sqrt(params.resistance_ohm))^2;
        end
    end
    if ~isfinite(heat_w)
        error('BatteryPower:Range', ...
            'Thermal heat generation is not representable as a finite double.');
    end
    if conductance == 0
        heat_delta = heat_w / capacitance * dt_s;
        if heat_delta == 0 && heat_w > 0
            heat_delta = heat_w * dt_s / capacitance;
        end
        temperature_c(index + 1) = temperature_c(index) + heat_delta;
    elseif x < 1e-6
        fade = -expm1(-x);
        if x == 0
            ratio = 1;
        else
            ratio = fade / x;
        end
        heat_delta = heat_w / capacitance * dt_s;
        if heat_delta == 0 && heat_w > 0
            heat_delta = heat_w * dt_s / capacitance;
        end
        cooling_delta = (params.ambient_c - temperature_c(index)) * fade;
        if isfinite(cooling_delta)
            base = temperature_c(index) + cooling_delta;
        else
            base = temperature_c(index) * decay + params.ambient_c * fade;
        end
        temperature_c(index + 1) = base + heat_delta * ratio;
    else
        steady_c = params.ambient_c + heat_w / conductance;
        difference = temperature_c(index) - steady_c;
        if isfinite(steady_c) && isfinite(difference)
            temperature_c(index + 1) = steady_c + difference * decay;
        else
            % Formal steady state or difference can overflow although
            % the exact finite-time weighted solution is representable.
            fade = -expm1(-x);
            heat_gain = heat_w / conductance;
            if isfinite(heat_gain)
                heat_gain = heat_gain * fade;
            else
                heat_delta = heat_w / capacitance * dt_s;
                if heat_delta == 0 && heat_w > 0
                    heat_delta = heat_w * dt_s / capacitance;
                end
                heat_gain = heat_delta * (fade / x);
            end
            temperature_c(index + 1) = temperature_c(index) * decay + ...
                params.ambient_c * fade + heat_gain;
        end
    end
    if ~isfinite(temperature_c(index + 1))
        error('BatteryPower:Range', ...
            'Thermal update is not representable as a finite double.');
    end
end
end
