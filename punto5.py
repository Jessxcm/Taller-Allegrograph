from franz.openrdf.connect import ag_connect
from franz.openrdf.query.query import QueryLanguage
with ag_connect('bd03',host='localhost', port='10035',user='bd03', password='$bd03!') as conn:
    print (conn.size())


query_string = """
PREFIX  class: <http://example.com/class/>
PREFIX  prop:  <http://example.com/property/> 
PREFIX  rdf:   <http://www.w3.org/1999/02/22-rdf-syntax-ns#> 
PREFIX  xsd: <http://www.w3.org/2001/XMLSchema#>

SELECT ?user_ret ?date_ret ?message ?content ?autor ?name ?date
WHERE { 
  ?autor prop:username ?name.
  ?message prop:date ?date.
  ?message prop:content ?content.
  ?message ^prop:writes ?autor.
  ?user_ret prop:username "maria@example.com"@en.
  ?user_ret ^prop:user/prop:date ?date_ret.
  ?user_ret ^prop:user/^prop:retweet ?message
  
}
"""

tuple_query = conn.prepareTupleQuery(QueryLanguage.SPARQL, query_string)
result = tuple_query.evaluate()
with result:
    for binding_set in result:
        user_ret = binding_set.getValue("user_ret")
        date_ret = binding_set.getValue("date_ret")
        message = binding_set.getValue("message")
        content = binding_set.getValue("content")
        autor = binding_set.getValue("autor")
        name = binding_set.getValue("name")
        date = binding_set.getValue("date")
        print("%s %s %s %s %s %s %s" % (user_ret,date_ret,message,content,autor,name,date))