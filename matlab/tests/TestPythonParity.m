classdef TestPythonParity < matlab.unittest.TestCase
    % Compare actual MATLAB execution with captured Python baseline values.
    properties
        Fixture
    end

    methods (TestClassSetup)
        function loadFixture(testCase)
            matlabRoot = fileparts(fileparts(mfilename('fullpath')));
            root = fileparts(matlabRoot);
            testCase.applyFixture(matlab.unittest.fixtures.PathFixture(matlabRoot));
            testCase.Fixture = jsondecode(fileread(fullfile(root, ...
                'tests', 'fixtures', 'python_matlab_parity.json')));
            fixture = testCase.Fixture;
            testCase.assertEqual(fixture.schema_version, 1);
            testCase.assertEqual(fixture.relative_tolerance, 1e-9);
            testCase.assertEqual(fixture.absolute_tolerance, 1e-12);
            testCase.assertNumElements(fixture.thermal, 6);
            testCase.assertNumElements(fixture.dc_link, 4);
            testCase.assertEqual(string({fixture.thermal.name}), ...
                ["ambient", "constant_heating", "cooling", ...
                "signed_current", "zero_resistance", "time_constant"]);
            testCase.assertEqual(string({fixture.dc_link.name}), ...
                ["reference", "zero_load", "small_drop", "large_capacitance"]);
        end
    end

    methods (Test)
        function thermalCasesMatchPython(testCase)
            cases = testCase.Fixture.thermal;
            for index = 1:numel(cases)
                item = cases(index);
                actual = battery_thermal_lumped(item.currents_a(:)', ...
                    item.dt_s, item.params, item.initial_c);
                expected = item.expected_c(:)';
                testCase.assertNotEmpty(expected);
                testCase.assertNumElements(expected, numel(item.currents_a) + 1);
                testCase.assertEqual(size(actual), size(expected));
                testCase.assertTrue(all(isfinite(actual)) && all(isfinite(expected)));
                bound = testCase.Fixture.absolute_tolerance + ...
                    testCase.Fixture.relative_tolerance * abs(expected);
                testCase.verifyLessThanOrEqual(abs(actual - expected), ...
                    bound, item.name);
            end
        end

        function dcLinkCasesMatchPython(testCase)
            cases = testCase.Fixture.dc_link;
            for index = 1:numel(cases)
                item = cases(index);
                values = num2cell(item.arguments);
                actual = dc_link_ripple(values{:});
                expected = [item.expected_ripple_vpp, ...
                    item.expected_minimum_capacitance_f];
                values = [actual.ripple_vpp, actual.minimum_capacitance_f];
                testCase.assertNumElements(item.arguments, 7);
                testCase.assertNumElements(values, 2);
                testCase.assertTrue(all(isfinite(values)) && all(isfinite(expected)));
                bound = testCase.Fixture.absolute_tolerance + ...
                    testCase.Fixture.relative_tolerance * abs(expected);
                testCase.verifyLessThanOrEqual(abs(values - expected), ...
                    bound, item.name);
            end
        end
    end
end
