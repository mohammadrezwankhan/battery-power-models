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
if isfinite(denominator) && denominator > 0
    ripple_vpp = current_pp_a / denominator;
else
    ripple_vpp = 0;
end
if ~isfinite(ripple_vpp) || ripple_vpp == 0
    % The final result can be representable even when the denominator
    % overflows or underflows; factorize without relaxing finite-value checks.
    exponent = log(current_pp_a) - log(8) - log(switching_hz) - log(capacitance_f);
    ripple_vpp = exp(exponent);
end
if ~isfinite(ripple_vpp) || ripple_vpp == 0
    error('BatteryPower:Range', ...
        'A nonzero ripple result is outside the finite double range.');
end
end
