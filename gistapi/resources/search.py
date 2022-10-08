from flask import jsonify
from flask_restful import Resource, marshal, reqparse
from helpers.gists import gists_for_user
from helpers.matcher import get_all_matched_gists
from serializers.gist_search_serailizer import search_api_fields


class GistSearchApi(Resource):
    def __init__(self) -> None:
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument(
            "username",
            type=str,
            required=True,
            help="No username provided",
            location="json",
        )
        self.reqparse.add_argument("pattern", type=str, default="", location="json")
        super().__init__()

    def post(self):
        request_args = self.reqparse.parse_args()
        start = request_args.get("start")
        limit = request_args.get("limit")
        results = {
            "status": "success",
            "username": request_args["username"],
            "pattern": request_args["pattern"],
            "matches": get_all_matched_gists(
                request_args["pattern"],
                gists_for_user(request_args["username"], page=start, per_page=limit),
            ),
        }
        return jsonify(marshal(results, search_api_fields))
