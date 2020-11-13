from franz.openrdf.connect import ag_connect
from franz.openrdf.query.query import QueryLanguage
with ag_connect('bd03',host='localhost', port='10035',user='bd03', password='$bd03!') as conn:
    print (conn.size())

query_string = """
PREFIX  res:   <http://example.com/resource/> 
PREFIX  class: <http://example.com/class/>
PREFIX  prop:  <http://example.com/property/> 
PREFIX  rdf:   <http://www.w3.org/1999/02/22-rdf-syntax-ns#> 
PREFIX  xsd: <http://www.w3.org/2001/XMLSchema#>

SELECT ?username ?country ?message ?content ?date ?username_ret ?date_ret ?country_ret
WHERE { ?user rdf:type class:User.
?message rdf:type class:Message .
?country rdf:type class:Country .
?message prop:content ?content.
?message prop:date ?date.
?user prop:username ?username.
?user prop:writes ?message.
?user prop:country ?country.
?message prop:retweet ?ret.
?ret    prop:user  ?user_ret.
?ret    prop:date  ?date_ret.
?user_ret rdf:type class:User.
?user_ret prop:username ?username_ret.
?country_ret rdf:type class:Country.
?user_ret prop:country ?country_ret.
FILTER(regex(str(?country), "Colombia" ) )
}
"""

tuple_query = conn.prepareTupleQuery(QueryLanguage.SPARQL, query_string)
result = tuple_query.evaluate()
with result:
    for binding_set in result:
        username = binding_set.getValue("username")
        country = binding_set.getValue("country")
        message = binding_set.getValue("message")
        content = binding_set.getValue("content")
        date = binding_set.getValue("date")
        username_ret = binding_set.getValue("username_ret")
        date_ret = binding_set.getValue("date_ret")
        country_ret = binding_set.getValue("country_ret")
        print("%s %s %s %s %s %s %s %s" % (username,country,message,content,date,username_ret,date_ret,country_ret))