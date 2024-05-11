 /**
 * @name sql-injection
 * @description this is just a test
 * @kind path-problem
 * @id this-is-1
 * @security-severity 5
 */
 
 import java
 import semmle.code.java.dataflow.FlowSources
 import semmle.code.java.security.QueryInjection
 import DataFlow::PathGraph
 
 
 class VulConfig extends TaintTracking::Configuration {
   VulConfig() { this = "SqlInjectionConfig" }
 
   override predicate isSource(DataFlow::Node src) { src instanceof RemoteFlowSource }
 
   override predicate isSink(DataFlow::Node sink) {
     exists(Method method, MethodAccess call |
       method.hasName("query")
       and
       call.getMethod() = method and
       sink.asExpr() = call.getArgument(0)
     )
   }

   override predicate isSanitizer(DataFlow::Node node) {
    node.getType() instanceof PrimitiveType or
    node.getType() instanceof BoxedType or
    node.getType() instanceof NumberType or
    exists(ParameterizedType pt| node.getType() = pt and pt.getTypeArgument(0) instanceof NumberType )

  }
 }
 
 
 from VulConfig config, DataFlow::PathNode source, DataFlow::PathNode sink
 where config.hasFlowPath(source, sink)
select source.getNode(), source, sink, "source"
// select source.getNode(), sink.getNode(), "在 $@ 到 $@ 的数据流路径中检测到潜在的 SQL 注入漏洞。", source, sink
