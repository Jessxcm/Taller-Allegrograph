from franz.openrdf.connect import ag_connect
from franz.openrdf.query.query import QueryLanguage
with ag_connect('bd03',host='localhost', port='10035',user='bd03', password='$bd03!') as conn:
    print (conn.size())


query_string = """
PREFIX  class: <http://example.com/class/>
PREFIX  prop:  <http://example.com/property/> 
PREFIX  rdf:   <http://www.w3.org/1999/02/22-rdf-syntax-ns#> 
PREFIX  xsd: <http://www.w3.org/2001/XMLSchema#>

SELECT ?followers ?names
WHERE { 
  ?follower prop:following/prop:user/prop:username "alejandro@example.com"@en.
  ?followers prop:username ?names.
  ?followers (prop:following/prop:user)* ?follower.
  
}
"""

tuple_query = conn.prepareTupleQuery(QueryLanguage.SPARQL, query_string)
result = tuple_query.evaluate()
with result:
    for binding_set in result:
        followers = binding_set.getValue("followers")
        names = binding_set.getValue("names")
        print("%s %s" % (followers,names))