from franz.openrdf.connect import ag_connect
from franz.openrdf.query.query import QueryLanguage
with ag_connect('bd03',host='localhost', port='10035',user='bd03', password='$bd03!') as conn:
    print (conn.size())

#queries 

#querie: Devuelve los datos de la cuenta del usuario.
query_string = """
PREFIX  class: <http://example.com/class/>
PREFIX  prop:  <http://example.com/property/> 
PREFIX  rdf:   <http://www.w3.org/1999/02/22-rdf-syntax-ns#> 
PREFIX  xsd: <http://www.w3.org/2001/XMLSchema#>

SELECT ?username ?profile ?country ?date
WHERE { ?user rdf:type class:User.
?user prop:username ?username.
?user prop:profile ?profile.
?user prop:date ?date.
?country rdf:type class:Country.
?user prop:country ?country.
FILTER regex(?username, "alejandro@example.com", "i")}
"""
print ("======================================================================================================================")
print ("DATOS DE LA CUENTA")
from franz.openrdf.query.query import QueryLanguage
tuple_query = conn.prepareTupleQuery(QueryLanguage.SPARQL, query_string)
result = tuple_query.evaluate()
with result:
    for binding_set in result:
        username = binding_set.getValue("username")
        profile = binding_set.getValue("profile")
        date = binding_set.getValue("date")
        country = binding_set.getValue("country")
        print ("======================================================================================================================")
        print("username: %s \nprofile: %s \ndate_created: %s \ncountry: %s" % (username, profile, date, country))
        print ("======================================================================================================================")


#querie: Devuelve todos los mensajes del usuario y sus respuestas si las ha tenido.
query_string = """
PREFIX  class: <http://example.com/class/>
PREFIX  prop:  <http://example.com/property/> 
PREFIX  rdf:   <http://www.w3.org/1999/02/22-rdf-syntax-ns#> 
PREFIX  xsd: <http://www.w3.org/2001/XMLSchema#>

SELECT ?message ?content ?date ?rcontent
WHERE { ?user rdf:type class:User.
?user prop:username ?username.
?message rdf:type class:Message .
?user prop:writes ?message.
?message prop:date ?date.
?message prop:content ?content
OPTIONAL { ?message prop:response ?resp.
           ?resp    prop:content  ?rcontent}.
FILTER regex(?username, "alejandro@example.com", "i")}
ORDER BY DESC(?date)"""

print ("======================================================================================================================")
print ("MENSAJES")
print ("======================================================================================================================")

from franz.openrdf.query.query import QueryLanguage
tuple_query = conn.prepareTupleQuery(QueryLanguage.SPARQL, query_string)
result = tuple_query.evaluate()
with result:
    for binding_set in result:
        message = binding_set.getValue("message")
        content = binding_set.getValue("content")
        date = binding_set.getValue("date")
        rcontent = binding_set.getValue("rcontent")
        print("%s %s %s %s" % (message, content, date, rcontent))

#querie: Devuelve los mensajes de los seguidores.
query_string = """
PREFIX  class: <http://example.com/class/>
PREFIX  prop:  <http://example.com/property/> 
PREFIX  rdf:   <http://www.w3.org/1999/02/22-rdf-syntax-ns#> 
PREFIX  xsd: <http://www.w3.org/2001/XMLSchema#>

SELECT ?username ?userfollow ?f_user ?f_content ?f_date
WHERE { ?user rdf:type class:User.
?user prop:username ?username.
?user prop:following ?followings.
?followings prop:user ?userfollow.
?userfollow prop:username ?f_user.
?userfollow prop:writes ?f_message.
?f_message prop:content ?f_content.
?f_message prop:date ?f_date.       
FILTER regex(?username, "alejandro@example.com", "i")}
ORDER BY DESC(?f_date)"""

print ("======================================================================================================================")
print ("MENSAJES DE LOS SEGUIDORES")
print ("======================================================================================================================")

from franz.openrdf.query.query import QueryLanguage
tuple_query = conn.prepareTupleQuery(QueryLanguage.SPARQL, query_string)
result = tuple_query.evaluate()
with result:
    for binding_set in result:
        f_user = binding_set.getValue("f_user")
        f_content = binding_set.getValue("f_content")
        f_date = binding_set.getValue("f_date")
        print("%s %s %s" % (f_user, f_content, f_date))


