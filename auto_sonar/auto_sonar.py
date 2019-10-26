import subprocess
import os


CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))

SCANNER_LIST = [
    'msbuild',
    'maven',
    'gradle',
    'ant',
    'sonar_scanner'
]

# TODO:  msbuild


def run_command(execution_array):
    try:
        return subprocess.run(execution_array).returncode
    except:
        return -1


class AutoSonar:
    def __init__(self, project_path='.', scanner=None, url='http://localhost:9000', token=None, key=None):
        self.project_path = os.path.abspath(project_path)
        self.scanner = scanner
        self.scanner_map = {
            'msbuild': self.run_msbuild,
            'maven': self.run_maven,
            'gradle': self.run_gradle,
            'ant': self.run_ant,
            'sonar_scanner': self.run_sonar_scanner
        }
        self.params = [f'-Dsonar.host.url={url}',
                       f'-Dsonar.projectBaseDir={self.project_path}']
        if token is not None:
            self.params.append(f'-Dsonar.login={token}')
        if key is not None:
            self.params.append(f'-Dsonar.projectKey={key}')

    def run(self):
        if self.scanner is not None:
            self.scanner_map[self.scanner]()
            return self.scanner
        for _, scanner in self.scanner_map.items():
            scanner()

    def run_msbuild(self):
        print(f'msbuild on path {self.project_path}')

    def run_maven(self):
        print(f'Trying Maven on path {self.project_path}...')
        execution_array = [
            'mvn', 'clean', 'verify',
            '-f', os.path.join(self.project_path, 'pom.xml'),
            'sonar:sonar', *self.params]
        code = run_command(execution_array)
        if code:
            print('Could not run Maven.')
        return code

    def run_gradle(self):
        print(f'Trying Gradle on path {self.project_path}...')
        execution_array = [
            os.path.join(self.project_path, 'gradlew'),
            'sonarqube', '-p', self.project_path,
            *self.params]
        code = run_command(execution_array)
        if code:
            print('Could not run Gradle.')
        return code

    def run_ant(self):
        print(f'Trying Ant on path {self.project_path}...')
        execution_array = [
            'ant', 'sonar',
            '-buildfile', os.path.join(self.project_path, 'build.xml'),
            *self.params]

        code = run_command(execution_array)
        if code:
            print('Could not run Ant.')
        return code

    def run_sonar_scanner(self):
        print(f'Trying Sonar Scanner on path {self.project_path}...')
        execution_array = [
            os.path.join(CURRENT_PATH, '../sonar-scanner/bin/sonar-scanner'),
            *self.params]
        code = run_command(execution_array)
        if code:
            print('Could not run Sonar Scanner.')
        return code
