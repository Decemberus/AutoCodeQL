# AutoCodeQL

## 项目介绍

项目的结构如下图所示

```

├─example-project
│  └─micro_service_seclab 一个java项目的测试用例
├─ql-query-example ql查询语句示例，这个查询语句主要用来查找springboot项目中的sql注入问题
├─result  输出结果目录
├─tools
│  └─CodeQLQuery.py 调用查询语句
│  └─DatabaseCreating codeql数据库构建
│  └─ExtractingResult 从sarif中提取有用信息并打印
│
├─autocodeql.py 项目主程序

```





如果想要查看项目效果的话，只需要指定codeql可执行文件的位置即可，如

```
-c "D:\CodeQL\Excusable\codeql\codeql.exe"
```

接下来项目会自动进行codeql数据库的构建，查询语句的执行，以及打印有用的信息

如果需要测试其他项目，则可以按照命令行的提示来指定，共有以下几个参数

```
'-c','--codeql_path',help = "codeql executable path"
'-j','--java_project_path',help = "the path of java project to be tested"
'-d','--database_path',help = "The location where the codeql database is generated"
'-r','--results_path',help= "The path to store the sarif results"
'-q','--query_path',help = "The path of the ql query statement"
```


待测试的java项目来自
https://github.com/l4yn3/micro_service_seclab.git


## 开发小日志

原本是想着直接把之前用VSCode codeql写的查询语句直接换成codeql cli来直接执行命令，但是却报的下面这个错误

```
(base) PS D:\Code_Project\Python\AutoCodeQL\qlproject\micro_service_seclab> codeql database analyze D:\Code_Project\Python\AutoCodeQL\qlproject\micro_service_seclab\qldb "D:\CodeQL\query\example-query\micro-qlpack.ql" --format=csv --output=codeql.csv
Running queries.
Compiling query plan for D:\CodeQL\query\example-query\micro-qlpack.ql.
[1/1] Found in cache: D:\CodeQL\query\example-query\micro-qlpack.ql.
Starting evaluation of example-query\micro-qlpack.ql.
[1/1 eval 4.5s] Evaluation done; writing results to example-query\micro-qlpack.bqrs.
Shutting down query evaluator.
Interpreting results.
A fatal error occurred: Could not process query metadata for D:\CodeQL\query\example-query\micro-qlpack.ql.
Error was: Cannot process query metadata for a query without the '@kind' metadata property. To learn more, see https://codeql.github.com/docs/writing-codeql-queries/metadata-for-codeql-queries/ [NO_KIND_SPECIFIED]
```

这个问题出现在ql语句的开头，必须要有这个开头才能够使用cli，而如果直接使用VSCode则不需要这个开头，也就在要看path的时候会用到@kind，而cli的话是强制要求使用的，这和直接用VSCode差别蛮大的

这里官方的文档里也有过说明

[Analyzing your code with CodeQL queries - GitHub Docs](https://docs.github.com/en/code-security/codeql-cli/getting-started-with-the-codeql-cli/analyzing-your-code-with-codeql-queries)

```
 /**
 * @name sql-injection
 * @description this is just a test
 * @kind path-problem
 * @id this-is-1
 * @security-severity 5
 */
```

命令的含义见这里[Metadata for CodeQL queries — CodeQL (github.com)](https://codeql.github.com/docs/writing-codeql-queries/metadata-for-codeql-queries/)

添加完以后就可以成功运行了

```
 codeql database analyze "D:\Code_Project\Python\AutoCodeQL\qlproject\micro_service_seclab\qldb" D:\CodeQL\query\example-query\micro-qlpack.ql --format=csv --output=codeql.csv

```

![image-20240510185707380](https://enjoyy-1322917755.cos.ap-nanjing.myqcloud.com/image-20240510185707380.png) 

得到了这些csv文件

```
"sql-injection","this is just a test","warning","source","/src/main/java/com/l4yn3/microserviceseclab/controller/IndexController.java","30","30","30","78"
"sql-injection","this is just a test","warning","source","/src/main/java/com/l4yn3/microserviceseclab/controller/IndexController.java","36","29","36","63"
"sql-injection","this is just a test","warning","source","/src/main/java/com/l4yn3/microserviceseclab/controller/IndexController.java","47","38","47","62"
"sql-injection","this is just a test","warning","source","/src/main/java/com/l4yn3/microserviceseclab/controller/IndexController.java","59","39","59","63"
"sql-injection","this is just a test","warning","source","/src/main/java/com/l4yn3/microserviceseclab/controller/IndexController.java","64","39","64","105"
```

[CodeQL CLI CSV output - GitHub Docs](https://docs.github.com/en/code-security/codeql-cli/using-the-advanced-functionality-of-the-codeql-cli/csv-output)

不过再后续学习中学长告诉我说静态分析里面有一个通用的格式叫SARIF，这个格式统一了静态分析工具输出结果，比csv更加的好用，教程我看的是微软写的一个教程[microsoft/sarif-tutorials: User-friendly documentation for the SARIF file format. (github.com)](https://github.com/microsoft/sarif-tutorials/tree/main)

蛮通俗易懂，也把主要的东西给讲好了

我的想法是从sarif中提取我们使用vscode的codeql相同的信息，然后输出为一个文件，也很好实现


最终的效果为
```
CodeFlow 6:
source: user  in src/main/java/com/l4yn3/microserviceseclab/controller/IndexController.java at "public List<Teacher> objectLomBok(@RequestBody Teacher user) {"  
dataflow1: user  in src/main/java/com/l4yn3/microserviceseclab/controller/IndexController.java at "return indexLogic.getTeacherById(user.getName());"  
dataflow2: parameter this  in src/main/java/com/l4yn3/microserviceseclab/data/Teacher.java at "private String name;"  
dataflow3: this.name  in src/main/java/com/l4yn3/microserviceseclab/data/Teacher.java at "private String name;"  
dataflow4: getName(...)  in src/main/java/com/l4yn3/microserviceseclab/controller/IndexController.java at "return indexLogic.getTeacherById(user.getName());"  
dataflow5: userName  in src/main/java/com/l4yn3/microserviceseclab/logic/IndexLogic.java at "public List<Teacher> getTeacherById(String userName) {"  
dataflow6: userName  in src/main/java/com/l4yn3/microserviceseclab/logic/IndexLogic.java at "return indexDb.getTeacherById(userName);"  
dataflow7: userName  in src/main/java/com/l4yn3/microserviceseclab/db/IndexDb.java at "public List<Teacher> getTeacherById(String userName) {"  
sink: sqlWithInt in src/main/java/com/l4yn3/microserviceseclab/db/IndexDb.java at "return jdbcTemplate.query(sqlWithInt, ROW_MAPPER_TEACHER);"  
```




