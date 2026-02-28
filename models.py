import uuid
from database import get_connection


class InventoryManager:

    def create_item(self, name, description, purchase_price, sale_price):
        if purchase_price <= 0 or sale_price <= 0:
            raise ValueError("Los precios deben ser mayores a 0")

        conn = get_connection()
        cursor = conn.cursor()

        item_id = str(uuid.uuid4())

        cursor.execute("""
            INSERT INTO items (id, name, description, purchase_price, sale_price)
            VALUES (?, ?, ?, ?, ?)
        """, (item_id, name, description, purchase_price, sale_price))

        conn.commit()
        conn.close()

        return item_id

    def get_all_items(self):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM items")
        rows = cursor.fetchall()

        conn.close()
        return rows
        
    def register_purchase(self, item_id, quantity):
        if quantity <= 0:
            raise ValueError("Cantidad inválida")

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT stock FROM items WHERE id = ?", (item_id,))
        result = cursor.fetchone()

        if not result:
            raise ValueError("Producto no encontrado")

        cursor.execute("""
            UPDATE items
            SET stock = stock + ?
            WHERE id = ?
        """, (quantity, item_id))

        cursor.execute("""
            INSERT INTO movements (id, item_id, type, quantity)
            VALUES (?, ?, 'purchase', ?)
        """, (str(uuid.uuid4()), item_id, quantity))

        conn.commit()
        conn.close()


    def register_sale(self, item_id, quantity):
        if quantity <= 0:
            raise ValueError("Cantidad inválida")

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT stock FROM items WHERE id = ?", (item_id,))
        result = cursor.fetchone()

        if not result:
            raise ValueError("Producto no encontrado")

        current_stock = result[0]

        if current_stock < quantity:
            raise ValueError("Stock insuficiente")

        cursor.execute("""
            UPDATE items
            SET stock = stock - ?
            WHERE id = ?
        """, (quantity, item_id))

        cursor.execute("""
            INSERT INTO movements (id, item_id, type, quantity)
            VALUES (?, ?, 'sale', ?)
        """, (str(uuid.uuid4()), item_id, quantity))

        conn.commit()
        conn.close()


    def get_movements(self, item_id):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT type, quantity, date
            FROM movements
            WHERE item_id = ?
            ORDER BY date DESC
        """, (item_id,))

        rows = cursor.fetchall()
        conn.close()
        return rows


    # ✅ AHORA SÍ ESTÁ DENTRO DE LA CLASE
    def get_all_movements_full(self):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT 
                items.name,
                movements.type,
                movements.quantity,
                movements.date,
                items.purchase_price,
                items.sale_price,
                items.stock
            FROM movements
            JOIN items ON movements.item_id = items.id
            ORDER BY movements.date DESC
        """)

        rows = cursor.fetchall()
        conn.close()
        return rows