def get_brands(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM brands ORDER BY name ASC;")
    return cursor.fetchall()


def add_sale(conn, week_id, day, brand_id, cost):
    cursor = conn.cursor()
    cursor.execute(
        """
            INSERT INTO sales (week_id, day, brand_id, cost)
            VALUES (?, ?, ?, ?)
            """,
        (week_id, day, brand_id, cost),
    )
    conn.commit()
