from database import TENANTS_DB_PATH, get_connection
from models.payment import Payment


class PaymentRepository:
	def __init__(self, db_path: str = TENANTS_DB_PATH):
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

    # maybe get rid of because you shouldn't be able to delete history
	def delete(self, payment_id: int) -> None:
		conn = get_connection(self.db_path)
		cursor = conn.cursor()
		cursor.execute("DELETE FROM payments WHERE id = ?", (payment_id,))
		conn.commit()
		conn.close()
