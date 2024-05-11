import subprocess


def codeqlquery(codeql_path,database_path,results_path,query_path):
    print("正在执行CodeQL扫描...")
    #codeql database analyze <database> --format=<format> \
    #--sarif-category=<language-specifier> --output=<output> \
    #<packs,queries>
    subprocess.run(
        [codeql_path, 'database', 'analyze', database_path, query_path, '--format=sarif-latest', f'--output={results_path}'],
        check=True)
    print("扫描完成。结果已保存至：", results_path)