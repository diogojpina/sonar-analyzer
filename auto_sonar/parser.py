import configparser
from argparse import ArgumentParser

from auto_sonar import SCANNER_LIST


def parse():
    config = configparser.ConfigParser()
    config.read('config.ini')

    url = "http://" + config['SONAR']['host'] + ":" + config['SONAR']['port']

    parser = ArgumentParser(
        description='Auto Analyser for sonar',
        prog='auto_sonar')
    parser.add_argument('-p', '--path', default='.')
    parser.add_argument('-s', '--scanner',
                        choices=SCANNER_LIST)
    parser.add_argument('-u', '--url', default=url)
    parser.add_argument('-t', '--token', default=None)
    parser.add_argument('-k', '--project_key', default=None)

    args = parser.parse_args()

    args.maven_path = config['MAVEN']['path']
    args.maven_skipTests = config['MAVEN']['skipTests']

    args.ant_path = config['ANT']['path']

    args.gradle_path = config['GRADLE']['path']

    args.scanner_path = config['SCANNER']['path']
    
    return args
