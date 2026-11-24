function ripple_vpp = triangular_current_ripple_vpp(current_pp_a, switching_hz, capacitance_f)
%TRIANGULAR_CURRENT_RIPPLE_VPP Ideal symmetric zero-mean capacitor-current ripple.
%   DELTA_VPP = DELTA_I_PP / (8 * F_SW * C), for the assumed triangle waveform.
%   ESR, ESL, switching transients, capacitor tolerance and real inverter
%   modulation are outside this simplified reference equation.

arguments
    current_pp_a (1,1) double {mustBeReal, mustBeFinite, mustBeNonnegative}
    switching_hz (1,1) double {mustBeReal, mustBeFinite, mustBePositive}
    capacitance_f (1,1) double {mustBeReal, mustBeFinite, mustBePositive}
end
if current_pp_a == 0
    ripple_vpp = 0;
    return;
end

denominator = 8 * switching_hz * capacitance_f;
if isfinite(denominator) && denominator >= realmin
    ripple_vpp = current_pp_a / denominator;
else
    ripple_vpp = 0;
end
if ~isfinite(ripple_vpp) || ripple_vpp == 0
    ripple_vpp = scaledPositiveRatio(current_pp_a, [8 switching_hz capacitance_f]);
end
if ~isfinite(ripple_vpp) || ripple_vpp == 0
    error('BatteryPower:Range', ...
        'A nonzero ripple result is outside the finite double range.');
end
end
