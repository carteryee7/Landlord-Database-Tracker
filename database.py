import sqlite3


def get_connection(db_path: str = "data/tenants.db"):
	return sqlite3.connect(db_path)


def create_tenants_table(conn: sqlite3.Connection):
	cursor = conn.cursor()
	cursor.execute(
		"""
		CREATE TABLE IF NOT EXISTS tenants (
			id INTEGER PRIMARY KEY,
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
	cursor.execute(
		"""
		CREATE TABLE IF NOT EXISTS payments (
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			tenant_id INTEGER NOT NULL,
			amount REAL NOT NULL,
			type TEXT NOT NULL,
			date TEXT NOT NULL,
			FOREIGN KEY (tenant_id) REFERENCES tenants (id)
		)
		"""
	)
	conn.commit()


def init_database(db_path: str = "data/tenants.db"):
	conn = get_connection(db_path)
	create_tenants_table(conn)
	return conn


def init_payments_database(db_path: str = "data/payments.db"):
	conn = get_connection(db_path)
	create_payments_table(conn)
	return conn