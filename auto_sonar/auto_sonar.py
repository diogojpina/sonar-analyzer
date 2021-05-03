import subprocess
import os
import pymysql


CURRENT_PATH = os.path.dirname(os.path.abspath(__file__))

SCANNER_LIST = [
    'msbuild',
    'maven',
    'gradle',
    'ant',
    'sonar_scanner'
]

def run_command(execution_array):
    try:
        return subprocess.run(execution_array).returncode
    except:
        return -1


class AutoSonar:
    def __init__(self, args):
        self.project_path = os.path.abspath(args.path)
        self.scanner = args.scanner
        self.scanner_map = {            
            'maven': self.run_maven,
            'gradle': self.run_gradle,
            'ant': self.run_ant,
#            'msbuild': self.run_msbuild,
#            'sonar_scanner': self.run_sonar_scanner
        }
        self.url = args.url
        self.params = [f'-Dsonar.host.url={args.url}']
        if args.token is not None:
            self.params.append(f'-Dsonar.login={args.token}')
        if args.project_key is not None:
            self.params.append(f'-Dsonar.projectKey={args.project_key}')

        self.args = args

    def run(self):
        self.path = self.project_path

        self.db = pymysql.connect("127.0.0.1","root","R4o9o9t5!","gitxplorer" )
        self.cursor = self.db.cursor(pymysql.cursors.DictCursor)
        self.cursor.execute("select id, name, full_name, clone_url from repository where language = 'java' and status = 1 and watchers_count >= 4 and analyzed = 0  limit 5;")    
        #self.cursor.execute("select id, name, full_name, clone_url from repository where id = 999999;")
        
        results = self.cursor.fetchall()
        for row in results:    
            sql = "update repository set analyzed = 2 where id = %s"
            self.cursor.execute(sql, (row['id']))
        self.db.commit()

        for row in results:            
            self.analyse(row)

        self.db.close()
        return 0
        

    def analyse(self, repository):
        self.project_path = self.path + '/' + repository['name']
        name = repository['name']
        full_name = repository['full_name'].replace('/', ':')
        folder_name = repository['full_name'].replace('/', '_')
        self.params.append(f'-Dsonar.projectKey={full_name}')
        self.params.append(f'-Dsonar.projectName={name}')
        self.params.append(f'-Dsonar.projectBaseDir={self.project_path}')

        print('')
        print(repository)

        self.clean(self.project_path)
        self.clone(repository['clone_url'], self.project_path)

        if self.scanner is not None:
            self.scanner_map[self.scanner]()
            return self.scanner
        for _, scanner in self.scanner_map.items():
            code = scanner()
            if (code == 0):
                sql = "update repository set analyzed = 1 where id = %s"
                self.cursor.execute(sql, (repository['id']))
                self.db.commit()
                return 0

        self.clean(self.project_path)
        return 1

    def clone(self, url, dir):
        execution_array = ['git', 'clone', url, dir]
        code = run_command(execution_array)
        if code:
            print('Could not run clone the project.')
        return code

    def clean(self, dir):
        execution_array = ['rm', '-Rf', dir]
        run_command(execution_array)

    def run_msbuild(self):
        print(f'msbuild on path {self.project_path}')

    def run_maven(self):
        pom_file = os.path.join(self.project_path, 'pom.xml')

        if (os.path.exists(pom_file) == False):
            print("It's not a Maven project")
            return 1

        print(f'Trying Maven on path {self.project_path}...')     
        execution_array = [
            self.args.maven_path, 'clean', 'verify',
            '-f', pom_file,
            'sonar:sonar', *self.params]
        if (self.args.maven_skipTests):
            execution_array.append('-DskipTests=true')

        code = run_command(execution_array)
        if code:
            print('Could not run Maven.')
        return code

    def run_gradle(self):
        build_file = os.path.join(self.project_path, 'build.gradle')
        if (os.path.exists(build_file) == False):
            print("It's not a Gradle project")
            return 1

        print(f'Trying Gradle on path {self.project_path}...')
        execution_array = [
            self.args.gradle_path, 'build', 
            '--build-file', build_file]
        print(execution_array)
        run_command(execution_array)

        execution_array = [
            self.args.scanner_path,
            '-Dsonar.login=admin', '-Dsonar.password=admin', 
            '-Dsonar.sources=src', '-Dsonar.java.binaries=build',
            *self.params] 

        code = run_command(execution_array)
        if code:
            print('Could not run Gradle.')
        return code

    def run_ant(self):
        build_file = os.path.join(self.project_path, 'build.xml')
        if (os.path.exists(build_file) == False):
            print("It's not an Ant project")
            return 1

        print(f'Trying Ant on path {self.project_path}...')
        execution_array = [
            self.args.ant_path, 'build', 
            '-buildfile', build_file]
        run_command(execution_array)

        execution_array = [
            self.args.scanner_path,
            '-Dsonar.login=admin', '-Dsonar.password=admin', 
            '-Dsonar.sources=src', '-Dsonar.java.binaries=target',
            *self.params]        

        code = run_command(execution_array)
        if code:
            print('Could not run Ant.')
        return code

    def run_sonar_scanner(self):
        print(f'Trying Sonar Scanner on path {self.project_path}...')
        execution_array = [
            self.args.scanner_path,
            *self.params]
        code = run_command(execution_array)
        if code:
            print('Could not run Sonar Scanner.')
        return code
