from flask import Flask, render_template, request, redirect
from database import initialize_database
from models import InventoryManager

app = Flask(__name__)
manager = InventoryManager()

initialize_database()

@app.route("/")
def index():
    items = manager.get_all_items()
    return render_template("index.html", items=items)


@app.route("/create", methods=["GET", "POST"])
def create():
    if request.method == "POST":
        manager.create_item(
            request.form["name"],
            request.form["description"],
            float(request.form["purchase_price"]),
            float(request.form["sale_price"])
        )
        return redirect("/")
    return render_template("create.html")


@app.route("/purchase/<item_id>", methods=["POST"])
def purchase(item_id):
    manager.register_purchase(item_id, int(request.form["quantity"]))
    return redirect("/")


@app.route("/sale/<item_id>", methods=["POST"])
def sale(item_id):
    manager.register_sale(item_id, int(request.form["quantity"]))
    return redirect("/")


@app.route("/movements/<item_id>")
def movements(item_id):
    data = manager.get_movements(item_id)
    return render_template("movements.html", movements=data)

@app.route("/export")
def export_movements():

    data = manager.get_all_movements_full()

    wb = Workbook()
    ws = wb.active
    ws.title = "Movimientos Inventario"

    headers = [
        "Product SKU",
        "Type",
        "Quantity",
        "Date",
        "Inventory Cost",
        "Price Sale",
        "Stock"
    ]

    ws.append(headers)

    for row in data:
        ws.append(row)

    file_path = "movimientos_inventario.xlsx"
    wb.save(file_path)

    return send_file(file_path, as_attachment=True)

import os

from flask import send_file
from openpyxl import Workbook
import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
    
