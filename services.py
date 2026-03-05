from models.payment import Payment
from repositories.payment_repository import PaymentRepository
from repositories.tenant_repository import TenantRepository


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
