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

        function scaledThermalProductsRetainFiniteTransients(testCase)
            tiny = eps(0);
            cases = [1e154, 1, 1e-308, 1e-308, 0, 0, 1e308;
                1e-200, 1e-200, 1e-308, 1e308, 0, 0, 1e16;
                0, 0, tiny, 0.5, tiny, 100, 100*exp(-0.5)];
            for row = cases.'
                params = struct('resistance_ohm', row(2), ...
                    'thermal_capacitance_j_per_k', row(3), ...
                    'cooling_conductance_w_per_k', row(5), 'ambient_c', 0);
                trace = battery_thermal_lumped(row(1), row(4), params, row(6));
                testCase.verifyEqual(trace(end), row(7), 'RelTol', 1e-14);
            end
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

        function finiteCoolingAcrossOppositeExtremeTemperatures(testCase)
            params = struct('resistance_ohm', 0, 'ambient_c', 1e308);
            actual = battery_thermal_lumped(0, 1, params, -1e308);
            decay = exp(-4 / 5000);
            fade = -expm1(-4 / 5000);
            expected = (-1e308 * decay) + (1e308 * fade);
            testCase.verifyEqual(actual(end), expected, 'RelTol', 1e-12);
        end

        function finiteTransientWithOverflowedEquilibrium(testCase)
            params = struct('resistance_ohm', 1, ...
                'thermal_capacitance_j_per_k', 1, ...
                'cooling_conductance_w_per_k', 1e-10, 'ambient_c', 0);
            actual = battery_thermal_lumped(1e150, 1e5, params, 0);
            expected = 1e305 * (-expm1(-1e-5)) / 1e-5;
            testCase.verifyEqual(actual(end), expected, 'RelTol', 1e-12);
        end

        function dedicatedDcLinkFunctionsNeedNoDummyArguments(testCase)
            reference = dc_link_ripple(20, 10000, 0.0022, 20000, 0.02, 800, 20);
            ripple = triangular_current_ripple_vpp(20, 10000, 0.0022);
            capacitance = minimum_capacitance_for_energy_pulse(20000, 0.02, 800, 20);
            testCase.verifyEqual(ripple, 0.11363636363636363, 'RelTol', 1e-12);
            testCase.verifyEqual(capacitance, 0.02531645569620253, 'RelTol', 1e-12);
            testCase.verifyEqual(ripple, reference.ripple_vpp, 'AbsTol', 1e-15);
            testCase.verifyEqual(capacitance, reference.minimum_capacitance_f, ...
                'AbsTol', 1e-15);
        end

        function dedicatedDcLinkFunctionsKeepBoundaryContracts(testCase)
            testCase.verifyEqual(triangular_current_ripple_vpp(0, 1e308, 1), 0);
            testCase.verifyEqual(minimum_capacitance_for_energy_pulse(0, 1, 1e308, 1), 0);
            testCase.verifyEqual(triangular_current_ripple_vpp(1, 1e308, 1), ...
                1.25e-309, 'RelTol', 1e-12);
            testCase.verifyEqual(minimum_capacitance_for_energy_pulse(1e308, 10, 800, 20), ...
                6.329113924050633e304, 'RelTol', 1e-12);
            testCase.verifyError( ...
                @() minimum_capacitance_for_energy_pulse(1000, 0.1, 800, 800), ...
                'BatteryPower:Range');
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
