from fastapi import FastAPI

from services.accessory_service import router as accessory_router
from services.brand_service import router as brand_router
from services.category_service import router as category_router
from services.history_receipts_service import router as history_receipts_router
from services.instrument_service import router as instrument_router
from services.inventory_receipt_service import router as inventory_receipt_router
from services.inventory_service import router as inventory_router
from services.receipt_service import router as receipt_router
from services.supplier_service import router as supplier_router
from services.user_service import router as user_router

app = FastAPI(
    title="Ortizo Store Management",
    version="0.0.1",
    description="This is an example of a CRUD using services for Ortizo music store."
)

# Routers de cada servicio
app.include_router(accessory_router)  # Servicio para accesorios
app.include_router(brand_router)  # Servicio para marcas
app.include_router(category_router)  # Servicio para categorías
app.include_router(history_receipts_router)  # Servicio para historial de recibos
app.include_router(instrument_router)  # Servicio para instrumentos
app.include_router(inventory_receipt_router)  # Servicio para Inventory_Receipt
app.include_router(inventory_router)  # Servicio para inventarios
app.include_router(receipt_router)  # Servicio para recibos
app.include_router(supplier_router)  # Servicio para proveedores
app.include_router(user_router)  # Servicio para usuarios
