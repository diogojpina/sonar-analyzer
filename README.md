# tcc-sonar
[![Build Status](https://travis-ci.org/caiohsramos/tcc-sonar.svg?branch=master)](https://travis-ci.org/caiohsramos/tcc-sonar)
[![codecov](https://codecov.io/gh/caiohsramos/tcc-sonar/branch/master/graph/badge.svg)](https://codecov.io/gh/caiohsramos/tcc-sonar)

## Usage
```
usage: auto_sonar [-h] [-p PATH] [-s {msbuild,maven,gradle,ant,sonar_scanner}]
                  [-u URL] [-t TOKEN] [-k PROJECT_KEY]

Auto Analyser for sonar

optional arguments:
  -h, --help            show this help message and exit
  -p PATH, --path PATH
  -s {msbuild,maven,gradle,ant,sonar_scanner}, --scanner {msbuild,maven,gradle,ant,sonar_scanner}
  -u URL, --url URL
  -t TOKEN, --token TOKEN
  -k PROJECT_KEY, --project_key PROJECT_KEY
```
## Default values
* PATH: `.`
* SCANNER: **ALL**
* URL: `http://localhost:9000`
* TOKEN: **NO TOKEN**
* PROJECT_KEY: **NO PROJECT KEY**

## Examples
### Using CLI
Analyse a Maven project:
```
python -m auto_sonar -p ../sonar-scanning-examples/sonarqube-scanner-maven/ -s maven
```

### Importing class AutoSonar
Analyse a Gradle project:
```python
# The scanner list is at auto_sonar.SCANNER_LIST
from auto_sonar import AutoSonar
auto_s = AutoSonar(
    project_path='../sonar-scanning-examples/sonarqube-scanner-gradle/', 
    scanner='gradle')
auto_s.run()
```
