from argparse import ArgumentParser

from auto_sonar import scanner_list


def parse():
    parser = ArgumentParser(
        description='Auto Analyser for sonar',
        prog='auto_sonar')
    parser.add_argument('-p', '--path', default='.')
    parser.add_argument('-s', '--scanner',
                        choices=[
                            'msbuild',
                            'maven',
                            'gradle',
                            'ant',
                            'jenkins',
                            'sonar_scanner'])
    parser.add_argument('-u', '--url', default='http://localhost:9000')
    parser.add_argument('-t', '--token', default=None)
    parser.add_argument('-k', '--project_key', default=None)

    args = parser.parse_args()
    return args
