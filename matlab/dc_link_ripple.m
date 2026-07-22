function result = dc_link_ripple(current_pp_a, switching_hz, capacitance_f, power_w, pulse_s, bus_v, allowed_drop_v)
%DC_LINK_RIPPLE Reference DC-link ripple and energy-pulse calculations.

arguments
    current_pp_a (1,1) double {mustBeNonnegative}
    switching_hz (1,1) double {mustBePositive}
    capacitance_f (1,1) double {mustBePositive}
    power_w (1,1) double {mustBeNonnegative}
    pulse_s (1,1) double {mustBeNonnegative}
    bus_v (1,1) double {mustBePositive}
    allowed_drop_v (1,1) double {mustBePositive}
end

assert(allowed_drop_v < bus_v, 'allowed_drop_v must be smaller than bus_v');
result.ripple_vpp = current_pp_a / (8 * switching_hz * capacitance_f);
final_v = bus_v - allowed_drop_v;
result.minimum_capacitance_f = 2 * power_w * pulse_s / (bus_v^2 - final_v^2);
end
