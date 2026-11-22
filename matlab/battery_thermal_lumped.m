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
x = scaled_product([conductance, dt_s], capacitance);
decay = exp(-x);
fade = -expm1(-x);
for index = 1:numel(currents_a)
    power_factors = [currents_a(index), currents_a(index), params.resistance_ohm];
    if x < 1e-6
        ratio = 1;
        if x > 0
            ratio = fade / x;
        end
        heat_gain = scaled_product([power_factors, dt_s, ratio], capacitance);
    else
        heat_gain = scaled_product([power_factors, fade], conductance);
    end
    base = temperature_c(index);
    if base ~= params.ambient_c && conductance > 0 && x < realmin
        ambient_term = scaled_product([params.ambient_c, conductance, dt_s], capacitance);
        initial_term = scaled_product([base, conductance, dt_s], capacitance);
        base = base + (ambient_term - initial_term);
    elseif base ~= params.ambient_c && x > 0
        base = base * decay + params.ambient_c * fade;
    end
    temperature_c(index + 1) = base + heat_gain;
    if x >= 1e-6
        steady = params.ambient_c + scaled_product(power_factors, conductance);
        transient = (temperature_c(index) - steady) * decay;
        reference = steady + transient;
        if isfinite(reference) && abs(reference) >= 0.125 * max(abs([steady, transient]))
            temperature_c(index + 1) = reference;
        end
    end
    if ~isfinite(temperature_c(index + 1))
        error('BatteryPower:Range', ...
            'Thermal update is not representable as a finite double.');
    end
end
end

function result = scaled_product(factors, divisor)
% Apply the combined binary exponent after bounded significand arithmetic.
if any(factors == 0)
    result = 0;
    return
end
[fractions, shifts] = log2(abs(factors));
[denominator, shift] = log2(divisor);
[mantissa, normalized_shift] = log2(prod(fractions) / denominator);
result = prod(sign(factors)) * pow2(mantissa, sum(shifts) - shift + normalized_shift);
end
