import subprocess


def databasecreating(codeql_path,database_path,java_project_path):
    print("正在创建CodeQL数据库...")
    try:
        #database create ~/CodeQL/databases/micro-service-seclab-database
        # --language="java"  --command="mvn clean install --file pom.xml" --source-root=~/CodeQL/micro-service-seclab/ --overright
        result = subprocess.run(
            [codeql_path, 'database', 'create', database_path, '--language=java', '--command=mvn clean install -Dmaven.test.skip=true --file pom.xml','--source-root', java_project_path],
            check=True)
    except:
        print("something error")
    print("数据库创建完成")


    # if "Successfully created" in result.stdout:
    #     print("数据库创建完成。")
    # else:
    #     print("数据库创建失败，请检查错误信息。")
