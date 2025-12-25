from flask import jsonify, request

from . import api_bp


@api_bp.get("/health")
def health():
    return jsonify(status="ok")


@api_bp.get("/items")
def list_items():
    q = request.args.get("q")
    items = [
        {"id": 1, "name": "Alpha"},
        {"id": 2, "name": "Bravo"},
        {"id": 3, "name": "Charlie"},
    ]
    if q:
        items = [i for i in items if q.lower() in i["name"].lower()]
    return jsonify(items=items)
