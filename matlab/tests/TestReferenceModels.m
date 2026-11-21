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

        function finiteAdiabaticHeatSurvivesIntermediateUnderflow(testCase)
            params = struct('resistance_ohm', 1e308, ...
                'thermal_capacitance_j_per_k', 1e-100, ...
                'cooling_conductance_w_per_k', 0, 'ambient_c', 0);
            trace = battery_thermal_lumped(1e-200, 1, params, 0);
            testCase.verifyEqual(trace(end), 1e8, 'RelTol', 1e-12);
            params.resistance_ohm = 1;
            params.thermal_capacitance_j_per_k = 1e308;
            trace = battery_thermal_lumped(1e-150, 1e308, params, 0);
            testCase.verifyEqual(trace(end), 1e-300, 'RelTol', 1e-12);
        end

        function adiabaticAndQuasiAdiabaticLimits(testCase)
            params = struct('cooling_conductance_w_per_k', 0);
            actual = battery_thermal_lumped([80 80], 5, params, 25);
            expected = [25, 25.0192, 25.0384];
            testCase.verifyEqual(actual, expected, 'AbsTol', 1e-12);
            params.cooling_conductance_w_per_k = 1e-14;
            testCase.verifyEqual(battery_thermal_lumped(80, 10, params, 25), ...
                [25, expected(end)], 'AbsTol', 1e-10);
        end

        function emptyProfileAndBooleanLikeValuesDoNotSlipThrough(testCase)
            testCase.verifyError(@() battery_thermal_lumped([], 1), ...
                'MATLAB:expectedRow');
            testCase.verifyError(@() battery_thermal_lumped(true, 1), ...
                'MATLAB:invalidType');
        end

        function dcLinkRetainsFiniteResultsWithOverflowingIntermediates(testCase)
            result = dc_link_ripple(1, 1e308, 1, 1e308, 10, 800, 20);
            testCase.verifyEqual(result.ripple_vpp, 1.25e-309, 'RelTol', 1e-12);
            testCase.verifyEqual(result.minimum_capacitance_f, ...
                6.329113924050633e304, 'RelTol', 1e-12);
            result = dc_link_ripple(0, 1e4, 0.01, 1e308, 1e308, 1e308, 5e307);
            testCase.verifyEqual(result.minimum_capacitance_f, 8 / 3, 'RelTol', 1e-12);
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

        function finiteInputsWithUnrepresentableResultsAreRejected(testCase)
            testCase.verifyError(@() battery_thermal_lumped(1e308, 1), ...
                'BatteryPower:Range');
            testCase.verifyError(@() dc_link_ripple(1, 1e-300, 1e-300, ...
                1000, 0.01, 800, 20), 'BatteryPower:Range');
            testCase.verifyError(@() dc_link_ripple(1, 1000, 0.01, ...
                1e308, 1e308, 800, 20), 'BatteryPower:Range');
        end
    end
end
