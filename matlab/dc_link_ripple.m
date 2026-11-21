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
% Preserve the seven-input struct API while delegating to standalone helpers.
result.ripple_vpp = triangular_current_ripple_vpp(current_pp_a, switching_hz, capacitance_f);
result.minimum_capacitance_f = ...
    minimum_capacitance_for_energy_pulse(power_w, pulse_s, bus_v, allowed_drop_v);
end
