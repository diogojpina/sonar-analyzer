from auto_sonar.parser import parse
from auto_sonar import AutoSonar


def main():
    args = parse()
    auto_s = AutoSonar(args)

    auto_s.run()


main()
