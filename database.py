LIST_BRANDS = [
    "Hugo",
    "Calvin",
    "Gucci",
    "Burberry",
    "Chloe",
    "Nautica",
    "Adidas",
    "David-Beckham",
    "Vera",
    "Davidoff",
    "Katy-Perry",
]


def initialize_database(conn):
    cursor = conn.cursor()

    # Create table preloaded with fixed brands
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS brands(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL
        );
        """
    )

    # Create table for weeks
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS weeks(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        start TEXT NOT NULL,
        end TEXT,
        state TEXT NOT NULL CHECK (state IN ('open', 'close'))
        );
        """
    )

    # Crete table for sales
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS sales(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        week_id INTEGER NOT NULL,
        day TEXT,
        brand_id INTEGER,
        cost REAL,
        FOREIGN KEY (week_id) REFERENCES weeks(id),
        FOREIGN KEY (brand_id) REFERENCES brands(id)
        );
        """
    )

    # Preload fixed brands
    for brand in LIST_BRANDS:
        cursor.execute("INSERT OR IGNORE INTO brands (name) VALUES (?);", (brand,))

    conn.commit()
