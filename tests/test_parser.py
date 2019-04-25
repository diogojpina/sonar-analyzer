import pytest
import auto_sonar


def test_parse_default(mocker):
    mocker.patch('sys.argv', new=['name'])
    args = auto_sonar.parser.parse()
    assert args.path == '.'
    assert args.scanner == None
    assert args.url == 'http://localhost:9000'
    assert args.token == None
    assert args.project_key == None


def test_parse(mocker):
    mocker.patch('sys.argv', new=[
        'name',
        '-p', 'mypath',
        '-s', 'maven',
        '-u', 'myurl',
        '-t', 'mytoken',
        '-k', 'mykey']
    )
    args = auto_sonar.parser.parse()
    assert args.path == 'mypath'
    assert args.scanner == 'maven'
    assert args.url == 'myurl'
    assert args.token == 'mytoken'
    assert args.project_key == 'mykey'
