import sqlite3


TENANTS_DB_PATH = "data/tenants.db"


def get_connection(db_path: str):
	conn = sqlite3.connect(db_path)
	conn.row_factory = sqlite3.Row
	conn.execute("PRAGMA foreign_keys = ON")
	return conn


def create_tenants_table(conn: sqlite3.Connection):
	cursor = conn.cursor()
	cursor.execute(
		"""
		CREATE TABLE IF NOT EXISTS tenants (
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			name TEXT NOT NULL,
			phone TEXT NOT NULL,
			unit TEXT NOT NULL,
			rent_cost REAL NOT NULL,
			amount_paid REAL NOT NULL,
			paid INTEGER NOT NULL CHECK (paid IN (0, 1))
		)
		"""
	)
	conn.commit()


def create_payments_table(conn: sqlite3.Connection):
	cursor = conn.cursor()

	# Recreate payments table if it exists without the foreign key constraint.
	cursor.execute("PRAGMA foreign_key_list(payments)")
	fk_rows = cursor.fetchall()
	if fk_rows == []:
		cursor.execute(
			"""
			SELECT name FROM sqlite_master
			WHERE type='table' AND name='payments'
			"""
		)
		if cursor.fetchone() is not None:
			cursor.execute("ALTER TABLE payments RENAME TO payments_old")

	cursor.execute(
		"""
		CREATE TABLE IF NOT EXISTS payments (
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			tenant_id INTEGER NOT NULL,
			amount REAL NOT NULL,
			type TEXT NOT NULL,
			date TEXT NOT NULL,
			FOREIGN KEY (tenant_id) REFERENCES tenants(id) ON DELETE CASCADE ON UPDATE CASCADE
		)
		"""
	)

	cursor.execute(
		"""
		SELECT name FROM sqlite_master
		WHERE type='table' AND name='payments_old'
		"""
	)
	if cursor.fetchone() is not None:
		cursor.execute(
			"""
			INSERT INTO payments (id, tenant_id, amount, type, date)
			SELECT id, tenant_id, amount, type, date
			FROM payments_old
			WHERE tenant_id IN (SELECT id FROM tenants)
			"""
		)
		cursor.execute("DROP TABLE payments_old")

	conn.commit()


def init_database(db_path: str = TENANTS_DB_PATH):
	conn = get_connection(db_path)
	create_tenants_table(conn)
	conn.close()


def init_payments_database(db_path: str = TENANTS_DB_PATH):
	conn = get_connection(db_path)
	create_payments_table(conn)
	conn.close()


def bootstrap() -> None:
	init_database(TENANTS_DB_PATH)
	init_payments_database(TENANTS_DB_PATH)
