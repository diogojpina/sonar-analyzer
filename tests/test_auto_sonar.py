import os

from auto_sonar import AutoSonar


def test_auto_sonar_default():
    auto_s = AutoSonar()
    assert auto_s.project_path == os.path.abspath('.')
    assert auto_s.scanner == None
    assert auto_s.params == ['-Dsonar.host.url=http://localhost:9000',
                             f'-Dsonar.projectBaseDir={auto_s.project_path}']
