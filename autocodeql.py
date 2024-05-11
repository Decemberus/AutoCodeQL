import argparse

from tools.CodeQLQuery import codeqlquery
from tools.DatabaseCreating import databasecreating
from tools.ExtractingResults import extract_vulnerabilities

bannerText="""
 █████╗ ██╗   ██╗████████╗ ██████╗  ██████╗ ██████╗ ██████╗ ███████╗ ██████╗ ██╗     
██╔══██╗██║   ██║╚══██╔══╝██╔═══██╗██╔════╝██╔═══██╗██╔══██╗██╔════╝██╔═══██╗██║     
███████║██║   ██║   ██║   ██║   ██║██║     ██║   ██║██║  ██║█████╗  ██║   ██║██║     
██╔══██║██║   ██║   ██║   ██║   ██║██║     ██║   ██║██║  ██║██╔══╝  ██║▄▄ ██║██║     
██║  ██║╚██████╔╝   ██║   ╚██████╔╝╚██████╗╚██████╔╝██████╔╝███████╗╚██████╔╝███████╗
╚═╝  ╚═╝ ╚═════╝    ╚═╝    ╚═════╝  ╚═════╝ ╚═════╝ ╚═════╝ ╚══════╝ ╚══▀▀═╝ ╚══════╝
                                                                                     
design by decemberus                                                                                                                                                                  
    """



if __name__ == '__main__':
    # codeql_path = "D:\CodeQL\Excusable\codeql\codeql.exe"
    # java_project_path = "D:\Code_Project\Python\AutoCodeQL\qlproject\micro_service_seclab"
    # database_path = "D:\Code_Project\Python\AutoCodeQL\qlproject\micro_service_seclab\qldb"
    # results_path = '.\result\codeql.sarif-latest'
    # query_path = 'D:\CodeQL\query\example-query\micro-qlpack.ql'
    print(bannerText)
    paser = argparse.ArgumentParser("")
    paser.add_argument('-c','--codeql_path',help = "codeql executable path",required= True)
    paser.add_argument('-j','--java_project_path',help = "the path of java project to be tested",required= True)
    paser.add_argument('-d','--database_path',help = "The location where the codeql database is generated",required= True)
    paser.add_argument('-r','--results_path',help= "The path to store the sarif results", default='../result/codeql.json')
    paser.add_argument('-q','--query_path',help = "The path of the ql query statement",required=True)

    args = paser.parse_args()
    codeql_path = args.codeql_path
    java_project_path = args.java_project_path
    database_path = args.database_path
    results_path = args.results_path
    query_path = args.query_path

    #构建codeql数据库
    #databasecreating(codeql_path,database_path,java_project_path)
    #执行codeql扫描
    #codeqlquery(codeql_path,database_path,results_path,query_path)
    #提取扫描结果
    extract_vulnerabilities(results_path)