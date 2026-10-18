classdef TestReferenceModels < matlab.unittest.TestCase
    methods (TestClassSetup)
        function addModelPath(testCase)
            modelPath = fileparts(fileparts(mfilename('fullpath')));
            testCase.applyFixture(matlab.unittest.fixtures.PathFixture(modelPath));
        end
    end

    methods (Test)
        function defaultThermalParametersMatchClosedForm(testCase)
            actual = battery_thermal_lumped([100 100], 1);
            expected = 25 + 7.5 * (1 - exp(-4 * (0:2) / 5000));
            testCase.verifyEqual(actual, expected, 'AbsTol', 1e-12);
        end

        function positionalStructControlsAmbientAndInitialTemperature(testCase)
            params = struct('ambient_c', 30);
            testCase.verifyEqual(battery_thermal_lumped(0, 1, params), [30 30]);
            actual = battery_thermal_lumped(0, 1, params, 40);
            expected = [40, 30 + 10 * exp(-4 / 5000)];
            testCase.verifyEqual(actual, expected, 'AbsTol', 1e-12);
        end

        function nonfiniteThermalValuesAreRejected(testCase)
            testCase.verifyError(@() battery_thermal_lumped(NaN, 1), ...
                'MATLAB:expectedFinite');
            testCase.verifyError(@() battery_thermal_lumped(0, Inf), ...
                'MATLAB:expectedFinite');
            testCase.verifyError(@() battery_thermal_lumped(0, 1, ...
                struct('resistance_ohm', NaN)), 'MATLAB:expectedFinite');
        end

        function smallVoltageDropDoesNotCancelToZero(testCase)
            result = dc_link_ripple(100, 10000, 0.01, 1000, 0.01, 800, 1e-15);
            expected = 2 * 1000 * 0.01 / (1e-15 * (1600 - 1e-15));
            testCase.verifyTrue(isfinite(result.minimum_capacitance_f));
            testCase.verifyEqual(result.minimum_capacitance_f, expected, ...
                'RelTol', 1e-12);
        end
    end
end
