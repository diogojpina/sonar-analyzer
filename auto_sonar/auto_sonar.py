import subprocess

scanner_list = [
    'msbuild',
    'maven',
    'gradle',
    'ant',
    'jenkins',
    'sonar_scanner'
]

# TODO: jenkins and msbuild


class AutoSonar:
    def __init__(self, project_path='.', scanner=None, url='http://localhost:9000', token=None):
        self.project_path = project_path
        self.scanner = scanner
        self.scanner_map = {
            'msbuild': self._run_msbuild,
            'maven': self._run_maven,
            'gradle': self._run_gradle,
            'ant': self._run_ant,
            # 'jenkins': self._run_jenkins,
            'sonar_scanner': self._run_sonar_scanner
        }
        self.params = [f'-Dsonar.host.url={url}']
        if token is not None:
            self.params.append(f'-Dsonar.login={token}')

    def run(self):
        if self.scanner is not None:
            self.scanner_map[self.scanner]()
            return self.scanner
        for _, scanner in self.scanner_map.items():
            scanner()

    def _run_msbuild(self):
        print(f'msbuild on path {self.project_path}')

    def _run_maven(self):
        print(f'Trying Maven on path {self.project_path}...')
        try:
            subprocess.run(['mvn', 'clean', 'verify',
                            'sonar:sonar', *self.params])
        except:
            print('Could not run Maven.')

    def _run_gradle(self):
        print(f'Trying Gradle on path {self.project_path}...')
        try:
            subprocess.run(
                ['gradle', 'sonarqube', *self.params])
        except:
            print('Could not run Gradle.')

    def _run_ant(self):
        print(f'Trying Ant on path {self.project_path}...')
        try:
            subprocess.run(
                ['ant', 'sonar', *self.params])
        except:
            print('Could not run Ant.')

    # def _run_jenkins(self):
    #     print(f'jenkins on path {self.project_path}')

    def _run_sonar_scanner(self):
        print(f'Trying Sonar Scanner on path {self.project_path}...')
        try:
            subprocess.run(
                ['sonar-scanner', *self.params])
        except:
            print('Could not run Sonar Scanner.')
