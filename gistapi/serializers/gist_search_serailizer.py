from flask_restful import fields



# fields for matches could also be nested 
# and then we'd define the structure of the nested response

search_api_fields = {
    "status": fields.String,
    "username": fields.String,
    "pattern": fields.String,
    "matches": fields.Raw,
}
