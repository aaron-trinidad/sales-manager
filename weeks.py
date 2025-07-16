from datetime import date, timedelta


def get_current_week_range():
    today = date.today()
    weekday = today.weekday()

    start_date = today - timedelta(days=weekday)
    end_date = start_date + timedelta(days=6)

    return start_date.isoformat(), end_date.isoformat()


def get_current_week(conn, start_date):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM weeks WHERE start = ?", (start_date,))
    return cursor.fetchone()


def create_current_week(conn, start_date, end_date):
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO weeks (start, end, state) VALUES (?, ?, 'open')",
        (start_date, end_date),
    )


def get_week_id(conn, start_date):
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM weeks WHERE start = ?;", (start_date,))
    row = cursor.fetchone()
    return row[0] if row else None


def close_current_week(conn, start_date):
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE weeks SET state = 'close' WHERE start = ? AND state = 'open'",
        (start_date,),
    )
