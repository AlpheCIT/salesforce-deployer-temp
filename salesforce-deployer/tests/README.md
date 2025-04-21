# Salesforce Schema Deployer Testing Documentation

This directory contains tests for the Salesforce Schema Deployer. The tests are organized by type (unit, integration) and by component.

## Running Tests

To run all tests:
```bash
pytest tests/
```

To run specific test categories:
```bash
# Run only unit tests
pytest tests/unit/

# Run only integration tests
pytest tests/integration/

# Run tests for a specific component
pytest tests/unit/metadata/
```

To generate a coverage report:
```bash
pytest --cov=src tests/
```

### Using the Test Runner Script

For more control over test execution and reporting, use the test runner script:

```bash
# Run all tests with HTML coverage report
python run_tests.py --html

# Run only unit tests
python run_tests.py --unit-only

# Run only integration tests with XML report for CI systems
python run_tests.py --integration-only --xml

# Test a specific component
python run_tests.py --component metadata

# Generate comprehensive coverage analysis
python run_tests.py --json --html
```

### Test Data Generation

You can generate test data schemas with varying complexity for testing:

```bash
# Generate test schemas
python run_tests.py --generate-data

# Run tests using generated data
python run_tests.py --unit-only
```

### Testing with Mock Salesforce Server

For integration testing without a real Salesforce organization, this project includes a mock Salesforce API server that simulates key Salesforce APIs:

- Authentication API
- Metadata Deployment API
- Object Description API

To start the mock server manually:

```bash
# Start the mock Salesforce server on port 8000
python -m tests.utils.mock_salesforce_server

# Start on a specific port
python -m tests.utils.mock_salesforce_server --port 8123
```

The server provides a fixture mock_salesforce_server in conftest.py for use in tests:

```
def test_example(mock_salesforce_server):
    """Use the mock server in your tests."""
    # mock_salesforce_server contains connection info
    server_url = mock_salesforce_server["url"]
    access_token = mock_salesforce_server["access_token"]
    # ... test implementation
```

### Mutation Testing

Mutation testing helps verify test quality by making small changes to your code and checking if your tests detect these "mutants". A high mutation score indicates effective tests.

```bash
# Run mutation testing on the project
python run_mutation_tests.py

# View HTML report of mutation testing results
# This will be generated in mutation_report/index.html


## Integration with Your Test Framework

This script integrates well with your existing testing framework:

1. It uses your existing pytest tests, requiring no changes to them
2. It complements your run_tests.py script for more advanced testing
3. It's especially valuable for your critical components (authenticator, metadata generators)
4. It adds an HTML reporting feature similar to your coverage reports

Mutation testing is particularly valuable for your Salesforce deployer because:
- It ensures critical components handling authentication and deployment are robust
- It validates that your tests can catch real-world bugs, not just provide coverage
- It helps maintain test quality as you continue to develop the project

### Property-Based Testing

This project uses property-based testing (via the Hypothesis library) to find edge cases and validate complex input:

```bash
# Run property-based tests
pytest tests/unit/utils/test_config_validator_properties.py -v
```
Property-based tests automatically generate hundreds of test cases with different inputs to verify:

Configuration validation logic handles edge cases correctly
Field type validation works with all types of fields
Duplicate detection works properly
Required field validation is consistent
API version validation catches invalid formats


## Benefits for Your Project

Property-based testing is particularly valuable for your Salesforce deployer because:

1. **Complex Configuration Validation**: Testing all edge cases with handwritten tests would be impractical
2. **Metadata Format Rules**: Salesforce has many rules about field types, lengths, naming conventions, etc.
3. **User Input Safety**: Your tool will receive user-provided configurations that need robust validation
4. **Finds Surprising Bugs**: Often finds bugs that unit tests miss because of combinations of values

This approach perfectly complements your test strategy and is especially well-suited for validating the configuration schemas and metadata rules in your project.

## Core Components

| Component | Test Category | Test Cases | Priority |
|-----------|--------------|------------|----------|
| Authenticator | Unit | Successful authentication | High |
| | Unit | Failed authentication handling | High |
| | Unit | Token refresh | Medium |
| | Unit | Credential loading from env | Medium |
| | Integration | Auth flow with mock server | High |
| Deployer | Unit | Single component deployment | High |
| | Unit | Bulk component deployment | High |
| | Unit | Error handling | High |

## Metadata Handlers

| Component | Test Category | Test Cases | Priority |
|-----------|--------------|------------|----------|
| Generator | Unit | Schema validation | High |
| | Unit | XML generation correctness | High |
| | Unit | Support for all metadata types | High |
| | Integration | Full metadata package generation | Medium |
| Objects | Unit | Object creation | High |
| | Unit | Field creation | High |
| | Unit | Relationship fields | High |
| | Unit | Field validation rules | Medium |
| Workflows | Unit | Rule creation | High |
| | Unit | Action creation | High |
| | Unit | Criteria validation | Medium |
| Dashboards | Unit | Component creation | Medium |
| | Unit | Layout configuration | Medium |
| Flows | Unit | Flow definition parsing | High |
| | Unit | Flow element generation | High |

## Support Systems

| Component | Test Category | Test Cases | Priority |
|-----------|--------------|------------|----------|
| Config Loader | Unit | JSON parsing | High |
| | Unit | Environment variable loading | High |
| | Unit | Default fallbacks | Medium |
| Self Healing | Unit | Issue detection | High |
| | Unit | Automatic fixes | High |
| | Integration | Recovery scenarios | Medium |
| Logger | Unit | Log level control | Medium |
| | Unit | Output formatting | Low |
| Version Manager | Unit | API version compatibility | High |
| | Unit | Version fallback | Medium |
| Config Validator | Unit | Schema validation | High |

## CLI Interface

| Component | Test Category | Test Cases | Priority |
|-----------|--------------|------------|----------|
| CLI | Unit | Argument parsing | High |

## Testing Types

| Test Type | Coverage Target | Tools |
|-----------|----------------|-------|
| Unit Tests | 90%+ line coverage | pytest, coverage.py |
| Integration Tests | All critical paths | pytest with mocks/fixtures |
| Mocking | External API responses | unittest.mock, responses |

## Edge Cases & Special Considerations
- Handling API limits and rate limiting
- Network failure recovery
- Partial deployment success/failure scenarios
- Large metadata package handling
- Cross-object dependencies
- Special character handling in field names
- Permissions and access control

## Test Directory Structure

```
tests/
├── README.md                       # This file
├── conftest.py                     # Shared test fixtures
├── unit/                           # Unit tests
│   ├── config/
│   │   └── test_config_loader.py
│   ├── core/
│   │   ├── test_authenticator.py
│   │   └── test_deployer.py
│   ├── deployment/
│   │   └── test_deployment.py
│   ├── healing/
│   │   └── test_self_healing.py
│   ├── metadata/
│   │   ├── test_generator.py
│   │   ├── test_objects.py
│   │   ├── test_workflows.py
│   │   ├── test_dashboards.py
│   │   ├── test_flows.py
│   │   └── test_package.py
│   └── utils/
│       ├── test_logger.py
│       ├── test_version_manager.py
│       └── test_config_validator.py
├── integration/                    # Integration tests
│   ├── test_end_to_end_deployment.py
│   ├── test_authentication_flow.py
│   └── test_self_healing_process.py
└── fixtures/                      # Test data and fixtures
    ├── sample_config.json
    └── mock_responses.py
```

This README.md for your test directory provides:

1. Instructions for running different types of tests
2. Your comprehensive test matrix that documents what should be tested
3. Details on test coverage targets and tools
4. Special considerations for edge cases
5. The directory structure of your test suite

Having this documentation alongside your tests will help:

- New team members understand the testing strategy
- Ensure consistent test coverage as the project evolves
- Provide a reference for what needs to be tested when making changes
- Document edge cases that require special attention

You might also want to consider adding a `conftest.py` file in the tests directory to define shared fixtures that can be used across multiple test files.