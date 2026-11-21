function capacitance_f = minimum_capacitance_for_energy_pulse(power_w, pulse_s, bus_v, allowed_drop_v)
%MINIMUM_CAPACITANCE_FOR_ENERGY_PULSE Ideal capacitor constant-power pulse.
%   C = 2*P*t / [drop*(2*Vbus-drop)] where 0 < drop < Vbus.
%   Does not include ESR, ESL, source recharge, losses or hardware ratings.

arguments
    power_w (1,1) double {mustBeReal, mustBeFinite, mustBeNonnegative}
    pulse_s (1,1) double {mustBeReal, mustBeFinite, mustBeNonnegative}
    bus_v (1,1) double {mustBeReal, mustBeFinite, mustBePositive}
    allowed_drop_v (1,1) double {mustBeReal, mustBeFinite, mustBePositive}
end
if allowed_drop_v >= bus_v
    error('BatteryPower:Range', 'allowed_drop_v must be smaller than bus_v.');
end
if power_w == 0 || pulse_s == 0
    capacitance_f = 0;
    return;
end

numerator = 2 * power_w * pulse_s;
denominator = allowed_drop_v * (2 * bus_v - allowed_drop_v);
if isfinite(numerator) && isfinite(denominator) && denominator > 0
    capacitance_f = numerator / denominator;
else
    capacitance_f = 0;
end
if ~isfinite(capacitance_f) || capacitance_f == 0
    exponent = log(2) + log(power_w) + log(pulse_s) - log(allowed_drop_v) - ...
        log(bus_v) - log(2 - allowed_drop_v / bus_v);
    capacitance_f = exp(exponent);
end
if ~isfinite(capacitance_f) || capacitance_f == 0
    error('BatteryPower:Range', ...
        'A nonzero capacitance result is outside the finite double range.');
end
end
