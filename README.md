# Webhook Reporter

## Description
Webhook Reporter is a GitHub Action that generates and sends comprehensive test coverage and test results reports to various messaging platforms. It parses coverage and test result data, creates a standardized report, and delivers it via webhooks to platforms like Discord, Slack, or Microsoft Teams.

## Features
- Supports multiple messaging platforms (Discord, Slack, Microsoft Teams)
- Parses coverage data from various testing frameworks
- Includes detailed test results alongside coverage information
- Easy to set up and integrate into existing GitHub Actions workflows

## Usage
To use this action in your workflow:

```yaml
steps:
  - uses: your-username/webhook-reporter@v1
    with:
      webhook_url: ${{ secrets.WEBHOOK_URL }}
      provider: 'discord'  # or 'slack' or 'teams'
      framework: 'pytest'  # or 'jacoco', 'cobertura', 'jest'
      coverage_file: 'path/to/coverage.xml'
      test_results_file: 'path/to/test-results.xml'
```

### Generating Test Results

For a fuller picture of your project's health, we recommend generating both coverage and test results files. Here's how to do it for various frameworks:

#### Pytest
To generate both coverage and test results:

```bash
pytest --cov=your_package --cov-report=xml:coverage.xml --junitxml=test-results.xml
```

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
For Cobertura (typically used with .NET):

```bash
dotnet test /p:CollectCoverage=true /p:CoverletOutputFormat=cobertura
```

Test results are typically generated automatically in the Visual Studio Test Platform's TRX format.

#### Jest (JavaScript)
To generate both coverage and test results with Jest:

```bash
jest --coverage --coverageReporters=cobertura --testResultsProcessor=jest-junit
```

Make sure to install `jest-junit` (`npm install --save-dev jest-junit`) and configure it in your `package.json`:

```json
"jest-junit": {
  "outputDirectory": "./test-results",
  "outputName": "test-results.xml"
}
```

## Configuration

| Input | Description | Required | Default |
|-------|-------------|----------|---------|
| `webhook_url` | The webhook URL for your messaging platform | Yes | N/A |
| `provider` | The messaging platform to use (`discord`, `slack`, or `teams`) | Yes | N/A |
| `framework` | The testing framework used (`pytest`, `jacoco`, `cobertura`, or `jest`) | Yes | N/A |
| `coverage_file` | Path to the coverage XML file | Yes | N/A |
| `test_results_file` | Path to the test results XML file | Yes | N/A |

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.