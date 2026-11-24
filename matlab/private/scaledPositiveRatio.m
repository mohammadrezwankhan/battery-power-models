function result = scaledPositiveRatio(numerator, denominator)
% Combine bounded significands before applying the net binary exponent.
[n, nExp] = log2(numerator);
[d, dExp] = log2(denominator);
[fraction, shift] = log2(prod(n) / prod(d));
result = pow2(fraction, sum(nExp) - sum(dExp) + shift);
end
