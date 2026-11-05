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
report.passed = isempty(issues.Issues) && ~isempty(results) && ...
    all([results.Passed]) && ~any([results.Incomplete]) && report.parity_verified;
report.claim_boundary = "Python baseline versus actual MATLAB reference models; no hardware validation.";
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
