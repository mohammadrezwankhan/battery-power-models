function report = security_numerical_gate()
%SECURITY_NUMERICAL_GATE Fail closed on analyzer issues or incomplete tests.
root = fileparts(fileparts(mfilename('fullpath')));
originalFolder = pwd;
originalPath = path;
cleanup = onCleanup(@() restore_context(originalFolder, originalPath));
cd(root);
addpath(fullfile(root, 'matlab'));
issues = codeIssues(fullfile(root, 'matlab'), ...
    CodeAnalyzerConfiguration="factory", IncludeSubfolders=true);
results = runtests(fullfile(root, 'matlab', 'tests'));
report.schema_version = 1;
report.matlab_release = string(version('-release'));
report.code_issues = table2struct(issues.Issues);
report.suppressed_issues = table2struct(issues.SuppressedIssues);
report.test_count = numel(results);
report.test_names = string({results.Name});
report.failed_count = sum([results.Failed]);
report.incomplete_count = sum([results.Incomplete]);
expectedNames = ["TestPythonParity/thermalCasesMatchPython", ...
    "TestPythonParity/dcLinkCasesMatchPython"];
parityTests = ismember(report.test_names, expectedNames);
fixture = jsondecode(fileread(fullfile(root, 'tests', 'fixtures', ...
    'python_matlab_parity.json')));
report.thermal_case_count = numel(fixture.thermal);
report.dc_link_case_count = numel(fixture.dc_link);
report.relative_tolerance = fixture.relative_tolerance;
report.absolute_tolerance = fixture.absolute_tolerance;
fixtureComplete = report.thermal_case_count == 6 && report.dc_link_case_count == 4 && ...
    report.relative_tolerance == 1e-9 && report.absolute_tolerance == 1e-12;
report.parity_verified = fixtureComplete && nnz(parityTests) == 2 && ...
    all(ismember(expectedNames, report.test_names)) && ...
    all([results(parityTests).Passed]) && ~any([results(parityTests).Incomplete]);
pythonFile = fullfile(root, 'hardening-artifacts', 'python-parity.json');
assert(isfile(pythonFile), 'SecurityGate:PythonCapture', ...
    'Current Python outputs must be captured before MATLAB execution.');
python = jsondecode(fileread(pythonFile));
[status, sourceCommit] = system('git rev-parse HEAD');
assert(status == 0 && strcmp(strtrim(sourceCommit), python.source_commit), ...
    'SecurityGate:PythonCapture', 'Python evidence must describe this checkout.');
assert(python.schema_version == 1 && isequal(python.passed, true) && ...
    python.relative_tolerance == 1e-9 && python.absolute_tolerance == 1e-12 && ...
    numel(python.thermal) == 6 && numel(python.dc_link) == 4, ...
    'SecurityGate:PythonCapture', 'Python evidence is incomplete or failed.');
thermal = repmat(struct(), 1, numel(fixture.thermal));
for index = 1:numel(fixture.thermal)
    item = fixture.thermal(index);
    assert(strcmp(item.name, python.thermal(index).name), ...
        'SecurityGate:PythonCapture', 'Thermal case names must match.');
    actual = battery_thermal_lumped(item.currents_a(:)', ...
        item.dt_s, item.params, item.initial_c);
    thermal(index).name = item.name;
    thermal(index).matlab_values = actual;
    thermal(index).baseline = compare_values(actual, item.expected_c(:)');
    thermal(index).current_python = ...
        compare_values(actual, python.thermal(index).values(:)');
end
dcLink = repmat(struct(), 1, numel(fixture.dc_link));
for index = 1:numel(fixture.dc_link)
    item = fixture.dc_link(index);
    assert(strcmp(item.name, python.dc_link(index).name), ...
        'SecurityGate:PythonCapture', 'DC-link case names must match.');
    argumentValues = num2cell(item.arguments);
    actual = dc_link_ripple(argumentValues{:});
    values = [actual.ripple_vpp, actual.minimum_capacitance_f];
    expected = [item.expected_ripple_vpp, item.expected_minimum_capacitance_f];
    dcLink(index).name = item.name;
    dcLink(index).matlab_values = values;
    dcLink(index).baseline = compare_values(values, expected);
    dcLink(index).current_python = compare_values(values, python.dc_link(index).values(:)');
end
allCases = [thermal, dcLink];
report.same_run_python_verified = all(arrayfun(@(item) ...
    item.baseline.passed && item.current_python.passed, allCases));
report.source_commit = strtrim(sourceCommit);
report.python_capture = python;
report.thermal_results = thermal;
report.dc_link_results = dcLink;
report.passed = isempty(issues.Issues) && ~isempty(results) && ...
    all([results.Passed]) && ~any([results.Incomplete]) && report.parity_verified && ...
    report.same_run_python_verified;
report.claim_boundary = "Original Python baseline and same-run Python/MATLAB reference outputs; no hardware validation.";
outputDirectory = fullfile(root, 'hardening-artifacts');
if ~isfolder(outputDirectory)
    mkdir(outputDirectory);
end
fileId = fopen(fullfile(outputDirectory, 'matlab-numerical-gate.json'), 'w');
assert(fileId >= 0, 'SecurityGate:Output', 'Cannot write numerical evidence.');
fileCleanup = onCleanup(@() fclose(fileId));
fprintf(fileId, '%s\n', jsonencode(report));
clear fileCleanup;
assert(report.passed, 'SecurityGate:Failed', ...
    'MATLAB analyzer, regression, or parity gate failed; inspect the evidence JSON.');
clear cleanup;
end

function restore_context(folder, originalPath)
cd(folder);
path(originalPath);
end

function result = compare_values(actual, expected)
assert(isequal(size(actual), size(expected)) && ~isempty(actual) && ...
    all(isfinite(actual)) && all(isfinite(expected)), ...
    'SecurityGate:ParityVectors', 'Parity vectors must have equal finite nonempty shapes.');
absolute = abs(actual - expected);
bound = 1e-12 + 1e-9 * abs(expected);
nonzero = expected ~= 0;
relative = absolute(nonzero) ./ abs(expected(nonzero));
result.reference_values = expected;
result.absolute_errors = absolute;
result.max_absolute_error = max(absolute);
result.max_relative_error_nonzero_reference = max([0, relative]);
result.max_error_fraction_of_bound = max(absolute ./ bound);
result.passed = all(absolute <= bound);
end
