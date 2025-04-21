# Salesforce Schema Deployer

A robust Python tool for managing Salesforce schema definitions, enabling extraction, comparison, and deployment of metadata configurations across Salesforce environments.

## Features

- **Schema Extraction**: Pull metadata definitions from Salesforce orgs
- **Intelligent Comparison**: Compare metadata across different environments
- **Selective Deployment**: Deploy only the intended changes to target orgs
- **Self-Healing**: Automatically handle dependencies and deployment order
- **Package Management**: Generate and deploy package.xml for Salesforce metadata

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/salesforce-deployer.git
cd salesforce-deployer

# Install dependencies
pip install -e .
```
## Basic Usage
```bash
# Extract metadata from source org
salesforce-deployer extract -c config.yaml -o source_org

# Deploy to target org
salesforce-deployer deploy -c config.yaml -s source_org -t target_org
```

### Configuration File
Create a YAML configuration file to specify the metadata types to process:
```
# config.yaml
objects:
  Account:
    fields: ['Name', 'Industry', 'CustomField__c']
  Contact:
    fields: ['FirstName', 'LastName', 'Email']

workflowRules:
  Account_Status_Update:
    criteria: "Account.Status__c = 'Active'"

dashboards:
  Sales_Dashboard:
    label: "Sales Performance"

lightningFlows:
  Lead_Process:
    description: "Lead qualification process"
```
### Authentication
The tool supports multiple authentication methods:

```
# Username/password flow
salesforce-deployer auth -u username -p password -s security_token -d production

# OAuth flow
salesforce-deployer auth --oauth -c consumer_key -s consumer_secret
```
## Architecture
The Salesforce Schema Deployer follows a modular architecture:

- **CLI Module**: Command-line interface and user interaction
- **Configuration**: Config loading and validation
- **Authentication**: Handles Salesforce authentication
- **Metadata Components**: Object definitions for various Salesforce metadata types
- **Extraction**: Pulls metadata from Salesforce orgs
- **Deployment**: Handles deployment to target orgs
- **Self-Healing**: Resolves dependencies and orders operations

## Development
Setup Development Environment

```
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -e ".[dev]"
```

### Running Tests
```
# Run all tests
pytest

# Run with coverage
pytest --cov=src

# Run specific test files
pytest tests/unit/metadata/test_package.py
```

### Coding Standards
We follow PEP 8 guidelines. Run linting with:
```
flake8 src tests
```

## API Specification Validation

This project uses Spectral to validate our OpenAPI specifications.

### Installation

```bash
# Install Spectral globally
npm install -g @stoplight/spectral-cli
```
## Usage
```
# Validate API specification
spectral lint api-specs/v1/salesforce-deployer-api.yaml
```

### CI/CD Integration
API specifications are automatically validated:
API specifications are automatically validated:
- When you run the "Validate OpenAPI Spec" VS Code task
- On GitHub through our GitHub Actions workflow
```
Congratulations on successfully implementing API specification validation! Your OpenAPI specification is now properly validated and ready for use in documentation tools, code generators, and API testing frameworks.Congratulations on successfully implementing API specification validation! Your OpenAPI specification is now properly validated and ready for use in documentation tools, code generators, and API testing frameworks.
```

## Setting Up a Mock Server
For your frontend development, you can immediately start working with a mock server based on this specification:
```
npm install -g @stoplight/prism-cli
prism mock api-specs/v1/salesforce-deployer-api.yaml
```

This mock server will:
- Validate requests against the schema
- Return example responses from the specification
- Allow frontend development to proceed independently of backend implementation
```
I've placed it right after the API Specification Validation section and before the Contributing section, since it's closely related to the API specification topic. I've also fixed the formatting issues that were present in your original README.md.I've placed it right after the API Specification Validation section and before the Contributing section, since it's closely related to the API specification topic. I've also fixed the formatting issues that were present in your original README.md.
```
Accessing the Mock API
The server runs at http://127.0.0.1:4010, but you must include the base path from the specification:

# Example: Authentication endpoint
curl -X POST http://127.0.0.1:4010/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"user@example.com","password":"myPassword123"}'

# Example: Get organizations
curl http://127.0.0.1:4010/api/v1/organizations \
  -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."

Note: Accessing the root URL (http://127.0.0.1:4010/) will return a "Route not resolved" error since the OpenAPI specification doesn't define any routes at the root path.

## API Code Generation

This project uses OpenAPI Generator to create server stubs and client SDKs from the API specification.

### Prerequisites

- Java Runtime Environment (JRE) 8 or later is required
- Download and install from: https://adoptium.net/temurin/releases/

### Setup

```bash
# Install OpenAPI Generator CLI
npm install -g @openapitools/openapi-generator-cli
```

### Prerequisites

- Java Development Kit (JDK) 11 or later is required (not just JRE)
- Download and install from: https://adoptium.net/temurin/releases/ (choose version 11 or higher)
- Ensure JAVA_HOME environment variable is set correctly

To check if your Java version is compatible, run:
```bash
./check-java-version.bat
```

## Contributing
1. Fork the repository
2. Create a feature branch (git checkout -b feature/amazing-feature)
3. Commit your changes (git commit -m 'Add some amazing feature')
4. Push to the branch (git push origin feature/amazing-feature)
5. Open a Pull Request

### License
This project is licensed under the MIT License - see the LICENSE file for details.