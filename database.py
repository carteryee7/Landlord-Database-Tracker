import sqlite3

from models.payment import Payment
from models.tenant import Tenant


TENANTS_DB_PATH = "data/tenants.db"
PAYMENTS_DB_PATH = "data/payments.db"


def get_connection(db_path: str):
	conn = sqlite3.connect(db_path)
	conn.row_factory = sqlite3.Row
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
	cursor.execute(
		"""
		CREATE TABLE IF NOT EXISTS payments (
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			tenant_id INTEGER NOT NULL,
			amount REAL NOT NULL,
			type TEXT NOT NULL,
			date TEXT NOT NULL
		)
		"""
	)
	conn.commit()


def init_database(db_path: str = TENANTS_DB_PATH):
	conn = get_connection(db_path)
	create_tenants_table(conn)
	conn.close()


def init_payments_database(db_path: str = PAYMENTS_DB_PATH):
	conn = get_connection(db_path)
	create_payments_table(conn)
	conn.close()


def bootstrap() -> None:
	init_database(TENANTS_DB_PATH)
	init_payments_database(PAYMENTS_DB_PATH)


class TenantRepository:
	def __init__(self, db_path: str = TENANTS_DB_PATH):
		self.db_path = db_path

	def create(self, tenant: Tenant) -> Tenant:
		conn = get_connection(self.db_path)
		cursor = conn.cursor()
		cursor.execute(
			"""
			INSERT INTO tenants (name, phone, unit, rent_cost, amount_paid, paid)
			VALUES (?, ?, ?, ?, ?, ?)
			""",
			(
				tenant.get_name(),
				tenant.get_phone(),
				tenant.get_unit(),
				tenant.get_rent_cost(),
				tenant.get_amount_paid(),
				tenant.get_paid(),
			),
		)
		tenant.set_id(cursor.lastrowid)
		conn.commit()
		conn.close()
		return tenant

	def get_by_id(self, tenant_id: int) -> Tenant | None:
		conn = get_connection(self.db_path)
		cursor = conn.cursor()
		cursor.execute("SELECT * FROM tenants WHERE id = ?", (tenant_id,))
		row = cursor.fetchone()
		conn.close()
		if row is None:
			return None
		return Tenant(
			id=row["id"],
			name=row["name"],
			phone=row["phone"],
			unit=row["unit"],
			rent_cost=row["rent_cost"],
			amount_paid=row["amount_paid"],
		)

	def list_all(self) -> list[Tenant]:
		conn = get_connection(self.db_path)
		cursor = conn.cursor()
		cursor.execute("SELECT * FROM tenants ORDER BY id")
		rows = cursor.fetchall()
		conn.close()
		return [
			Tenant(
				id=row["id"],
				name=row["name"],
				phone=row["phone"],
				unit=row["unit"],
				rent_cost=row["rent_cost"],
				amount_paid=row["amount_paid"],
			)
			for row in rows
		]

	def update(self, tenant: Tenant) -> None:
		if tenant.get_id() is None:
			raise ValueError("Tenant must have an id to update")

		conn = get_connection(self.db_path)
		cursor = conn.cursor()
		cursor.execute(
			"""
			UPDATE tenants
			SET name = ?, phone = ?, unit = ?, rent_cost = ?, amount_paid = ?, paid = ?
			WHERE id = ?
			""",
			(
				tenant.get_name(),
				tenant.get_phone(),
				tenant.get_unit(),
				tenant.get_rent_cost(),
				tenant.get_amount_paid(),
				tenant.get_paid(),
				tenant.get_id(),
			),
		)
		conn.commit()
		conn.close()

	def delete(self, tenant_id: int) -> None:
		conn = get_connection(self.db_path)
		cursor = conn.cursor()
		cursor.execute("DELETE FROM tenants WHERE id = ?", (tenant_id,))
		conn.commit()
		conn.close()


class PaymentRepository:
	def __init__(self, db_path: str = PAYMENTS_DB_PATH):
		self.db_path = db_path

	def create(self, payment: Payment) -> Payment:
		if payment.get_tenant_id() is None:
			raise ValueError("Payment must have tenant_id before create")

		conn = get_connection(self.db_path)
		cursor = conn.cursor()
		cursor.execute(
			"""
			INSERT INTO payments (tenant_id, amount, type, date)
			VALUES (?, ?, ?, ?)
			""",
			(
				payment.get_tenant_id(),
				payment.get_amount(),
				payment.get_type(),
				payment.get_date(),
			),
		)
		payment.set_id(cursor.lastrowid)
		conn.commit()
		conn.close()
		return payment

	def get_by_id(self, payment_id: int) -> Payment | None:
		conn = get_connection(self.db_path)
		cursor = conn.cursor()
		cursor.execute("SELECT * FROM payments WHERE id = ?", (payment_id,))
		row = cursor.fetchone()
		conn.close()
		if row is None:
			return None
		return Payment(
			id=row["id"],
			tenant_id=row["tenant_id"],
			amount=row["amount"],
			type=row["type"],
			date=row["date"],
		)

	def list_all(self) -> list[Payment]:
		conn = get_connection(self.db_path)
		cursor = conn.cursor()
		cursor.execute("SELECT * FROM payments ORDER BY id")
		rows = cursor.fetchall()
		conn.close()
		return [
			Payment(
				id=row["id"],
				tenant_id=row["tenant_id"],
				amount=row["amount"],
				type=row["type"],
				date=row["date"],
			)
			for row in rows
		]

	def list_by_tenant_id(self, tenant_id: int) -> list[Payment]:
		conn = get_connection(self.db_path)
		cursor = conn.cursor()
		cursor.execute("SELECT * FROM payments WHERE tenant_id = ? ORDER BY id", (tenant_id,))
		rows = cursor.fetchall()
		conn.close()
		return [
			Payment(
				id=row["id"],
				tenant_id=row["tenant_id"],
				amount=row["amount"],
				type=row["type"],
				date=row["date"],
			)
			for row in rows
		]

	def update(self, payment: Payment) -> None:
		if payment.get_id() is None:
			raise ValueError("Payment must have an id to update")

		conn = get_connection(self.db_path)
		cursor = conn.cursor()
		cursor.execute(
			"""
			UPDATE payments
			SET tenant_id = ?, amount = ?, type = ?, date = ?
			WHERE id = ?
			""",
			(
				payment.get_tenant_id(),
				payment.get_amount(),
				payment.get_type(),
				payment.get_date(),
				payment.get_id(),
			),
		)
		conn.commit()
		conn.close()

	def delete(self, payment_id: int) -> None:
		conn = get_connection(self.db_path)
		cursor = conn.cursor()
		cursor.execute("DELETE FROM payments WHERE id = ?", (payment_id,))
		conn.commit()
		conn.close()


class TenantService:
	def __init__(self, tenant_repository: TenantRepository, payment_repository: PaymentRepository):
		self.tenant_repository = tenant_repository
		self.payment_repository = payment_repository

	def add_payment(self, tenant_id: int, payment: Payment) -> None:
		tenant = self.tenant_repository.get_by_id(tenant_id)
		if tenant is None:
			raise ValueError(f"Tenant {tenant_id} not found")

		payment.set_tenant_id(tenant_id)
		self.payment_repository.create(payment)

		tenant.set_amount_paid(tenant.get_amount_paid() + payment.get_amount())
		self.tenant_repository.update(tenant)