# Webhook Reporter

## Description
Webhook Reporter is a versatile GitHub Action designed to generate and send detailed test coverage and test result reports to multiple messaging platforms. It seamlessly parses coverage and test result data, standardizes the reports, and delivers them through webhooks to platforms such as Discord, Slack, or Microsoft Teams.


## Features
- Multi-platform support (Discord, Slack, Microsoft Teams)
- Parses coverage data from multiple testing frameworks (e.g., JaCoCo, Cobertura, Clover)
- Combines both test results and coverage information in a unified report
- Simple setup and integration into any GitHub Actions workflow

## Usage
To use this action in your workflow:

```yaml
steps:
  - uses: your-username/webhook-reporter@v1
    with:
      webhook_url: ${{ secrets.WEBHOOK_URL }}
      provider: 'discord'  # Can also be 'slack' or 'teams'
      coverage_file: 'path/to/coverage.xml'
      test_results_file: 'path/to/test-results.xml'

# This action will parse the provided files and send a report to the specified webhook URL. Ensure the files are generated before this step.
# If any file is missing or an error occurs during processing, the action will log the issue for troubleshooting.
```
> **Note:** Ensure your webhook URL is stored securely as a GitHub Secret (e.g., `WEBHOOK_URL`).


### Generating Test Results

For comprehensive insights into your project's health, it's highly recommended to generate both coverage and test results files. Below are examples for several common testing frameworks:

#### Pytest
To generate both coverage and test results:

```bash
pytest --cov=your_package --cov-report=xml:coverage.xml --junitxml=test-results.xml
```
The above command runs `pytest` with coverage generation and outputs both coverage and test results in XML format, which can then be used by the Webhook Reporter.

#### JaCoCo (Java)
For JaCoCo, you typically configure it in your build tool. Here's an example for Maven:

```xml
<plugin>
    <groupId>org.jacoco</groupId>
    <artifactId>jacoco-maven-plugin</artifactId>
    <version>0.8.7</version>
    <executions>
        <execution>
            <goals>
                <goal>prepare-agent</goal>
            </goals>
        </execution>
        <execution>
            <id>report</id>
            <phase>test</phase>
            <goals>
                <goal>report</goal>
            </goals>
        </execution>
    </executions>
</plugin>
```

And for test results with Surefire:

```xml
<plugin>
    <groupId>org.apache.maven.plugins</groupId>
    <artifactId>maven-surefire-plugin</artifactId>
    <version>3.0.0-M5</version>
    <configuration>
        <redirectTestOutputToFile>true</redirectTestOutputToFile>
    </configuration>
</plugin>
```

#### Cobertura

```bash
dotnet test /p:CollectCoverage=true /p:CoverletOutputFormat=cobertura
```

Test results are typically generated automatically in the Visual Studio Test Platform's TRX format.

#### Jest (JavaScript)
To generate coverage and test results with Jest, use either JSON or JUnit reporters, depending on your needs.

##### JSON (Default)
Generate the default JSON coverage and test results:
```bash
jest --coverage --json --outputFile=results.json
```
For outputFile you can name it anything but please keep it consistent with what you will be providing into the `test_results` field.

##### JUNIT
To generate both coverage and test results with Jest:

```bash
jest --coverage --coverageReporters=cobertura --testResultsProcessor=jest-junit
```
This example generates coverage using the `cobertura` reporter and formats test results with `jest-junit` for Webhook Reporter to process.


>`Alias: --collectCoverage. Indicates that test coverage information should be collected and reported in the output. Optionally pass <boolean> to override option set in configuration.`

[more information](https://jestjs.io/docs/cli#--coverageproviderprovider)
Make sure to install `jest-junit` (`npm install --save-dev jest-junit`) and configure it in your `package.json`:

###### You can specify the file name and location details inside package.json *like* below:
```json
"jest-junit": {
  "outputDirectory": "./test-results",
  "outputName": "test-results.xml"
}
```

## Configuration

| Input               | Description                                                      | Required | Default |
|---------------------|------------------------------------------------------------------|----------|---------|
| `webhook_url`       | The webhook URL for your messaging platform (Discord, Slack, Teams) | Yes      | N/A     |
| `provider`          | The messaging platform to send the report to (`discord`, `slack`, `teams`) | Yes      | N/A     |
| `coverage_file`     | Path to the coverage XML file (e.g., `coverage.xml`)               | Yes      | N/A     |
| `test_results_file` | Path to the test results XML file (e.g., `test-results.xml`)       | Yes      | N/A     |


## Support
Webhook Reporter supports a variety of testing and coverage frameworks by recognizing common report file formats (e.g., Cobertura, JUnit). This means it works with any framework that outputs these standard formats, even if the framework itself isn't listed explicitly.

### Coverage Report Support
Webhook Reporter parses coverage reports using these file formats:
- **Cobertura XML**: Automatically generated by frameworks like Pytest and Jest.
- **JaCoCo XML**: Typically generated by Java frameworks using JaCoCo.
- **Clover XML**: Supported for coverage reports produced by Jest.

### Test Result Report Support
Webhook Reporter can handle test results in these formats:
- **JUnit XML**: Used by many frameworks, including JUnit (Java) and others that generate this format.
- **JSON**: Supported for frameworks like Jest when using the default JSON output.

### Example Frameworks:
- **Pytest**: Coverage generated in Cobertura format (`coverage.xml`); test results can be produced in JUnit XML if needed but are not required.
- **Jest**: Coverage supported through both Cobertura and Clover formats, with test results in JUnit XML or JSON.
- **JaCoCo**: Native JaCoCo coverage report format supported.
- **Unittest**: Test results can be captured via third-party tools that convert output to JUnit XML.

If your framework produces output in one of these formats, it is supported, even if the framework itself is not explicitly listed here.

## Contributing
Contributions are always welcome! If you'd like to contribute:
### Pre-requisites
* Get a webhook url to test your changes with.

### Code Review
1. Clone this repo
2. Create a new branch (`git checkout -b feature/change-name`)
    - for example `git checkout -b  feature/coverage-parser-jest`
3. Make your changes
4. Open a Pull Request
For major changes, please open an issue first to discuss your proposal.


### Generate an .env at root of the folder with following format:
``` bash
INPUT_PROVIDER="[PROVIDER NAME]" #discord, slack, teams
INPUT_WEBHOOK_URL="[WEBHOOK URL]"
INPUT_COVERAGE_FILE="./data/[COVERAGE-FILE]" # ADD THE EXTENSION
INPUT_TEST_RESULTS="./data/[TEST-RESULT-FILE-NAME]" # ADD THE EXTENSION
INPUT_COVERAGE_THRESHOLD=65 # 65 % for example
GITHUB_REPOSITORY='[USER-NAME/REPO-NAME]'
GITHUB_SHA='[SOME SHA]'
GITHUB_REF='refs/pull/38/merge'
GITHUB_ACTOR='[GITHUB USER-NAME]'
GITHUB_ACTOR_ID=
GITHUB_RUN_ID=
GITHUB_ACTION='random action'
GITHUB_EVENT_NAME='pull_request'
```
## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.