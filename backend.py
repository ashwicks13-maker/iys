from flask import Flask, request, Response
import sqlite3
import json
import os

app = Flask(__name__)

# Render için DB path (root veya /opt/render/project/src)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DB_FILES = [
    os.path.join(BASE_DIR, "iys_part_0.db"),
    os.path.join(BASE_DIR, "iys_part_1.db"),
    os.path.join(BASE_DIR, "iys_part_2.db"),
    os.path.join(BASE_DIR, "iys_part_3.db"),
    os.path.join(BASE_DIR, "iys_part_4.db"),
    os.path.join(BASE_DIR, "iys_part_5.db"),
    os.path.join(BASE_DIR, "iys_part_6.db"),
]


def query_db(db, where, params):
    conn = sqlite3.connect(db)
    cur = conn.cursor()

    cur.execute(f"SELECT * FROM data WHERE 1=1 {where}", params)
    rows = cur.fetchall()

    cols = [d[0] for d in cur.description]
    conn.close()

    return [dict(zip(cols, r)) for r in rows]


def query_all(where, params):
    result = []

    for db in DB_FILES:
        if os.path.exists(db):
            try:
                result += query_db(db, where, params)
            except:
                pass

    return result


@app.route("/search", methods=["GET"])
def search():
    name = request.args.get("name")
    phone = request.args.get("phone")
    city = request.args.get("city")

    where = ""
    params = []

    if name:
        where += " AND (name LIKE ? OR fullname LIKE ?)"
        params += [f"%{name}%", f"%{name}%"]

    if phone:
        where += " AND phone LIKE ?"
        params.append(f"%{phone}%")

    if city:
        where += " AND city LIKE ?"
        params.append(f"%{city}%")

    result = query_all(where, params)

    return Response(
        json.dumps({"count": len(result), "data": result}, ensure_ascii=False),
        content_type="application/json; charset=utf-8"
    )


@app.route("/")
def home():
    return {"status": "ok"}


# 🔥 RENDER FIX
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
