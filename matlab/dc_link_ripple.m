function result = dc_link_ripple(current_pp_a, switching_hz, capacitance_f, power_w, pulse_s, bus_v, allowed_drop_v)
%DC_LINK_RIPPLE Reference DC-link ripple and energy-pulse calculations.

arguments
    current_pp_a (1,1) double {mustBeReal, mustBeFinite, mustBeNonnegative}
    switching_hz (1,1) double {mustBeReal, mustBeFinite, mustBePositive}
    capacitance_f (1,1) double {mustBeReal, mustBeFinite, mustBePositive}
    power_w (1,1) double {mustBeReal, mustBeFinite, mustBeNonnegative}
    pulse_s (1,1) double {mustBeReal, mustBeFinite, mustBeNonnegative}
    bus_v (1,1) double {mustBeReal, mustBeFinite, mustBePositive}
    allowed_drop_v (1,1) double {mustBeReal, mustBeFinite, mustBePositive}
end

assert(allowed_drop_v < bus_v, 'allowed_drop_v must be smaller than bus_v');
ripple_denominator = 8 * switching_hz * capacitance_f;
if ~isfinite(ripple_denominator) || ripple_denominator == 0
    error('BatteryPower:Range', ...
        'Ripple denominator is not representable as a positive finite double.');
end
result.ripple_vpp = current_pp_a / ripple_denominator;
energy_denominator = allowed_drop_v * (2 * bus_v - allowed_drop_v);
if ~isfinite(energy_denominator) || energy_denominator == 0
    error('BatteryPower:Range', ...
        'Capacitance denominator is not representable as a positive finite double.');
end
result.minimum_capacitance_f = 2 * power_w * pulse_s / energy_denominator;
if ~isfinite(result.ripple_vpp) || ...
        (current_pp_a > 0 && result.ripple_vpp == 0) || ...
        ~isfinite(result.minimum_capacitance_f) || ...
        (power_w > 0 && pulse_s > 0 && result.minimum_capacitance_f == 0)
    error('BatteryPower:Range', ...
        'A nonzero result is outside the finite double range.');
end
end
