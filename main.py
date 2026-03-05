import database
from repositories.tenant_repository import TenantRepository
from repositories.payment_repository import PaymentRepository
from services import TenantService
from models.tenant import Tenant
from models.payment import Payment

database.bootstrap()

tenant_repository = TenantRepository()
payment_repository = PaymentRepository()
tenant_service = TenantService(tenant_repository, payment_repository)

tenant = Tenant("Carter Yee", "978-809-8387", "B5", 1200.00, 1000.00)
tenant_repository.create(tenant)

rent_payment = Payment(amount=200.00, type="Venmo", date="2026-03-04")
tenant_id = tenant.get_id()
if tenant_id is None:
	raise ValueError("Tenant ID was not set after save")
tenant_service.add_payment(tenant_id, rent_payment)

for saved_tenant in tenant_repository.list_all():
	print(
		saved_tenant.get_id(),
		saved_tenant.get_name(),
		saved_tenant.get_amount_paid(),
		saved_tenant.get_paid(),
	)
