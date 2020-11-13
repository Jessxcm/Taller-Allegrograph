from franz.openrdf.connect import ag_connect
from franz.openrdf.query.query import QueryLanguage
with ag_connect('bd03',host='localhost', port='10035',user='bd03', password='$bd03!') as conn:
    print (conn.size())


#2. Listar los mensajes que un usuario dado puso desde el 1º de mayo de 2018 y, en caso de haber recibido
#réplicas a esos mensajes, el texto de las réplicas.


query_string = """
PREFIX  class: <http://example.com/class/>
PREFIX  prop:  <http://example.com/property/> 
PREFIX  rdf:   <http://www.w3.org/1999/02/22-rdf-syntax-ns#> 
PREFIX  xsd: <http://www.w3.org/2001/XMLSchema#>

SELECT ?user ?username ?message ?content ?date ?rcontent
WHERE { ?user rdf:type class:User.
?user prop:username ?username.
?message rdf:type class:Message .
?user prop:writes ?message.
?message prop:date ?date.
?message prop:content ?content
OPTIONAL { ?message prop:response ?resp.
           ?resp    prop:content  ?rcontent}.
FILTER regex(?username, "alejandro@example.com", "i")
FILTER (?date>="2018-05-01"^^xsd:date)
}
"""

tuple_query = conn.prepareTupleQuery(QueryLanguage.SPARQL, query_string)
result = tuple_query.evaluate()
with result:
    for binding_set in result:
        user = binding_set.getValue("user")
        username = binding_set.getValue("username")
        message = binding_set.getValue("message")
        content = binding_set.getValue("content")
        date = binding_set.getValue("date")
        rcontent = binding_set.getValue("rcontent")

        print("%s %s %s %s %s %s" % (user,username, message,content,date,rcontent))