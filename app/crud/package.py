from app.db.base import conn, session
from app.models.package import Package
from app.schemas.package import Package as schemaPackage
from app.services.modbusMaster import Master
from app.exceptions.DBException import DBException
from pymodbus.exceptions import ModbusException

def read_all():
    try:
        all_packages = session.query(Package).all()
        return all_packages
    except Exception as e:
        session.rollback()
        raise DBException("Error al leer todos los paquetes", e)

def read_one(package_id: int):
    try:
        scale = session.query(Package).filter(Package.package_id == package_id).first()
        return scale
    except Exception as e:
        session.rollback()
        raise DBException(f"Error al leer el paquete {package_id}", e)

def create_package(name: str, expected_weight: float, minimum_weight: float, maximum_weight):
    try:
        package = Package(name=name, expected_weight=expected_weight, minimum_weight=minimum_weight, maximum_weight=maximum_weight)
        session.add(package)
        session.commit()
        return package
    except Exception as e:
        session.rollback()
        raise DBException("Error al crear el paquete", e)

def delete_package(package_id: int):
    try:
        package = session.query(Package).filter(Package.package_id == package_id).first()
        if package:
            package.active = False
            session.commit()
            return True
        return False
    except Exception as e:
        session.rollback()
        raise DBException(f"Error al eliminar el paquete {package_id}", e)

def restore_package(package_id: int):
    try:
        package = session.query(Package).filter(Package.package_id == package_id).first()
        if package:
            package.active = True
            session.commit()
            return True
        return False
    except Exception as e:
        session.rollback()
        raise DBException(f"Error al restaurar el paquete {package_id}", e)

def update_package(name: str, expected_weight: float, minimum_weight: float, maximum_weight: float, package_id: int):
    try:
        package = session.query(Package).filter(Package.package_id == package_id).first()
        package.name = name
        package.expected_weight = expected_weight
        package.minimum_weight = minimum_weight
        package.maximum_weight = maximum_weight
        session.commit()
        try:
            Master.update_package(package)
        except ModbusException as e:
            print(f"Error de Modbus al actualizar paquete: {e}")
        except Exception as e:
            print(f"Error inesperado al actualizar paquete en Modbus: {e}")
    except Exception as e:
        session.rollback()
        raise DBException(f"Error al actualizar el paquete {package_id}", e)

