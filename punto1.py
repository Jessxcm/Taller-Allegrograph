#from mainTaller import *
from franz.openrdf.connect import ag_connect
from franz.openrdf.query.query import QueryLanguage
with ag_connect('bd03',host='localhost', port='10035',user='bd03', password='$bd03!') as conn:
    print (conn.size())

#1. Listar todos los mensajes de un hashtag dado en orden cronológico

query_string = """
PREFIX  class: <http://example.com/class/>
PREFIX  prop:  <http://example.com/property/> 
PREFIX  rdf:   <http://www.w3.org/1999/02/22-rdf-syntax-ns#> 
PREFIX  xsd: <http://www.w3.org/2001/XMLSchema#>

SELECT ?message ?hashtag ?date
WHERE { ?message rdf:type class:Message .
?message prop:hashtag ?hashtag.
?message prop:date ?date
FILTER regex(?hashtag, "amistad", "i")  }
ORDER BY ASC(?date)"""

tuple_query = conn.prepareTupleQuery(QueryLanguage.SPARQL, query_string)
result = tuple_query.evaluate()
with result:
    for binding_set in result:
        message = binding_set.getValue("message")
        hashtag = binding_set.getValue("hashtag")
        date = binding_set.getValue("date")
        print("%s %s %s" % (message, hashtag, date))