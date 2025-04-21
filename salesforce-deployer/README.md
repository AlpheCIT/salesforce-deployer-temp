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

## Contributing
1. Fork the repository
2. Create a feature branch (git checkout -b feature/amazing-feature)
3. Commit your changes (git commit -m 'Add some amazing feature')
4. Push to the branch (git push origin feature/amazing-feature)
5. Open a Pull Request

### License
This project is licensed under the MIT License - see the LICENSE file for details.