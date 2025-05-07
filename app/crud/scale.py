from sqlalchemy.orm import Session
from app.models.scale import Scale
from app.db.base import conn, session
from app.schemas.scale import Scale as schemaScale
from app.models.package import Package
from app.services.modbusMaster import Master

def read_all():
    all_scales = session.query(Scale).all()
    return all_scales

def read_one(scale_id: int):
    scale = session.query(Scale).filter(Scale.scale_id == scale_id).first()
    return scale

def create_scale(name: str, packages: list[int], slave_address: int):
    packages = session.query(Package).filter(Package.package_id.in_(packages)).all()
    scale = Scale(name=name, slave_address=slave_address, packages=packages)
    session.add(scale)
    session.commit()
    Master.update_packages_for_scale(scale.packages, scale.slave_address)
    return read_one(scale.scale_id)

def get_last_slave_address():
    return session.query(Scale).order_by(Scale.slave_address.asc()).first().slave_address

def update_scale(name: str, packages_ids: list[int], scale_id: int):
    packages = session.query(Package).filter(Package.package_id.in_(packages_ids)).all()
    scale = session.query(Scale).filter(Scale.scale_id == scale_id).first()
    scale.name = name
    scale.packages = packages
    session.commit()
    print(f"Scale {scale.name} updated with packages: {[package.name for package in packages]}")
    Master.update_packages_for_scale(packages, scale.slave_address)

def delete_scale(scale_id: int):
    scale = session.query(Scale).filter(Scale.scale_id == scale_id).first()
    if scale:
        session.delete(scale)
        session.commit()
        return True
    return False
