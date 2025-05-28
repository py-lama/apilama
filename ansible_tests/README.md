# APILama Ansible Tests

This directory contains Ansible playbooks and tasks to test all endpoints of the APILama service. These tests help ensure that the API is functioning correctly and can be used for regression testing, continuous integration, and deployment verification.

## Prerequisites

- Ansible 2.9 or higher
- Running instance of APILama (and its dependent services)
- Python requests library (`pip install requests`)

## Test Structure

- `apilama_test_playbook.yml`: Main playbook that orchestrates all tests
- `file_operations_tests.yml`: Tests for file-related endpoints
- `directory_operations_tests.yml`: Tests for directory-related endpoints
- `shell_operations_tests.yml`: Tests for shell command execution
- `bexy_tests.yml`: Tests for BEXY code execution
- `getllm_tests.yml`: Tests for PyLLM text generation
- `devlama_tests.yml`: Tests for PyLama model execution

## Running the Tests

### Running All Tests

```bash
ansible-playbook apilama_test_playbook.yml
```

### Running with Custom API URL

```bash
ansible-playbook apilama_test_playbook.yml -e "api_base_url=http://localhost:8081"
```

### Running Specific Test Groups

To run only specific test groups, you can use tags (requires adding tags to the playbook tasks) or create a custom playbook that includes only the desired test files.

## Test Coverage

These tests cover the following APILama endpoints:

1. **Health Check**
   - GET /api/health

2. **File Operations**
   - GET /api/files (List files)
   - GET /api/file (Get file content)
   - POST /api/file (Create/update file)
   - DELETE /api/file (Delete file)

3. **Directory Operations**
   - GET /api/shellama/directory (Get directory info)
   - POST /api/shellama/directory (Create directory)
   - DELETE /api/shellama/directory (Delete directory)

4. **Shell Operations**
   - POST /api/shellama/shell (Execute shell command)

5. **BEXY Operations**
   - GET /api/bexy/health (Check BEXY health)
   - POST /api/bexy/execute (Execute Python code)

6. **PyLLM Operations**
   - GET /api/getllm/health (Check PyLLM health)
   - POST /api/getllm/generate (Generate text)

7. **PyLama Operations**
   - GET /api/devlama/health (Check PyLama health)
   - GET /api/devlama/models (List models)
   - POST /api/devlama/execute (Execute model)

## Extending the Tests

To add new tests or extend existing ones:

1. Create a new task file or modify an existing one
2. Add the new task file to the main playbook
3. Ensure proper error handling and result validation

## Troubleshooting

- If tests fail, check that all required services are running
- Verify the API URLs are correct
- Check for proper authentication if required
- Increase verbosity with `-v`, `-vv`, or `-vvv` flags for more detailed output
