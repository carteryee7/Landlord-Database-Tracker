from database import TENANTS_DB_PATH, get_connection
from models.tenant import Tenant


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
