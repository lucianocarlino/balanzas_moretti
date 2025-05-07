from app.db.base import conn, session
from app.models.package import Package
from app.schemas.package import Package as schemaPackage
from app.services.modbusMaster import Master

def read_all():
    all_packages = session.query(Package).all()
    return all_packages

def read_one(package_id: int):
    scale = session.query(Package).filter(Package.package_id == package_id).first()
    return scale

def create_package(name: str, expected_weight: float, minimum_weight: float, maximum_weight):
    package = Package(name=name, expected_weight=expected_weight, minimum_weight=minimum_weight, maximum_weight=maximum_weight)
    session.add(package)
    session.commit()
    return package

def delete_package(package_id: int):
    package = session.query(Package).filter(Package.package_id == package_id).first()
    if package:
        session.delete(package)
        session.commit()
        return True
    return False

def update_package(name: str, expected_weight: float, minimum_weight: float, maximum_weight: float, package_id: int):
    package = session.query(Package).filter(Package.package_id == package_id).first()
    package.name = name
    package.expected_weight = expected_weight
    package.minimum_weight = minimum_weight
    package.maximum_weight = maximum_weight
    session.commit()
    Master.update_package(package)
    
    
