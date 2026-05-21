from sqlalchemy.orm import Session
from app.models.scale import Scale
from app.db.base import conn, session
from app.schemas.scale import Scale as schemaScale
from app.models.package import Package
from app.services.modbusMaster import Master
from app.services.httpScale import HttpScale
from app.exceptions.DBException import DBException
from pymodbus.exceptions import ModbusException

def read_all():
    try:
        all_scales = session.query(Scale).all()
        return all_scales
    except Exception as e:
        session.rollback()
        raise DBException("Error al leer todas las balanzas", e)

def read_one(scale_id: int):
    try:
        scale = session.query(Scale).filter(Scale.scale_id == scale_id).first()
        return scale
    except Exception as e:
        session.rollback()
        raise DBException(f"Error al leer la balanza {scale_id}", e)

def create_scale(name: str, packages: list[int], slave_address: int):
    try:
        packages = session.query(Package).filter(Package.package_id.in_(packages)).all()
        scale = Scale(name=name, slave_address=slave_address, packages=packages)
        session.add(scale)
        session.commit()
        try:
            Master.update_packages_for_scale(scale.packages, scale.slave_address)
        except ModbusException as e:
            print(f"Error de Modbus al actualizar paquetes en balanza: {e}")
        except Exception as e:
            print(f"Error inesperado al actualizar paquetes en balanza: {e}")
        return read_one(scale.scale_id)
    except Exception as e:
        session.rollback()
        raise DBException("Error al crear la balanza", e)

def get_last_slave_address():
    try:
        return session.query(Scale).order_by(Scale.slave_address.asc()).first().slave_address
    except Exception as e:
        session.rollback()
        raise DBException("Error al obtener la última dirección de esclavo", e)

def update_scale(name: str, packages_ids: list[int], scale_id: int):
    try:
        packages = session.query(Package).filter(Package.package_id.in_(packages_ids)).all()
        scale = session.query(Scale).filter(Scale.scale_id == scale_id).first()
        scale.name = name
        scale.packages = packages
        session.commit()
        print(f"Scale {scale.name} updated with packages: {[package.name for package in packages]}")
        try:
            if scale.comunicacion != "HTTP":
                Master.update_packages_for_scale(packages, scale.slave_address)
            else:
                HttpScale.load_packages(scale)
        except ModbusException as e:
            print(f"Error de Modbus al actualizar paquetes en balanza: {e}")
        except Exception as e:
            print(f"Error inesperado al actualizar paquetes en balanza: {e}")
    except Exception as e:
        session.rollback()
        raise DBException(f"Error al actualizar la balanza {scale_id}", e)

def delete_scale(scale_id: int):
    try:
        scale = session.query(Scale).filter(Scale.scale_id == scale_id).first()
        if scale:
            scale.active = False
            session.commit()
            return True
        return False
    except Exception as e:
        session.rollback()
        raise DBException(f"Error al eliminar la balanza {scale_id}", e)

def restore_scale(scale_id: int):
    try:
        scale = session.query(Scale).filter(Scale.scale_id == scale_id).first()
        if scale:
            scale.active = True
            session.commit()
            return True
        return False
    except Exception as e:
        session.rollback()
        raise DBException(f"Error al restaurar la balanza {scale_id}", e)

def get_scale_packages(scale_id: int):
    try:
        scale = session.query(Scale).filter(Scale.scale_id == scale_id).first()
        return scale.packages
    except Exception as e:
        session.rollback()
        raise DBException(f"Error al leer la balanza {scale_id}", e)

