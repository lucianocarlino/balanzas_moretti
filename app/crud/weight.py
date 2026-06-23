from datetime import datetime, timedelta
from sqlalchemy import DateTime
from app.models.weight import Weight
from app.models.package import Package
from app.models.scale import Scale
from app.db.base import session
from app.exceptions.DBException import DBException
from app.schemas.weight import PushWeights, HttpWeight


def read_all(limit: int = 100000, init: DateTime = None, end: DateTime = None, package_id: int = None,
             scale_id: int = None):
    try:
        query = session.query(Weight)

        if (init and end):
            query = query.filter(Weight.date_time >= init).filter(Weight.date_time <= end)

        if package_id:
            query = query.filter(Weight.package_id == package_id)

        if scale_id:
            query = query.filter(Weight.scale_id == scale_id)

        return query.limit(limit).all()
    except Exception as e:
        session.rollback()
        raise DBException("Error al leer los pesos", e)

def write_weight(weights):
    update_packages = []
    try:
        data = []
        for scale in weights:
            if scale == []:
                continue
            scale_id = scale[0]
            scale.pop(0)
            for weight in scale:
                if weight[0] > 0:
                    package_obj = session.query(Package).filter(Package.package_id == weight[0]).first()
                    scale_obj = session.query(Scale).filter(Scale.scale_id == scale_id).first()
                    if package_obj is None or scale_obj is None:
                        print(
                            f"Package or Scale not found for weight entry: {weight}, scale_id: {scale_id}, package_obj: {package_obj}, scale_obj: {scale_obj}")
                        update_packages.append(scale_id)
                        continue
                    else:
                        data.append(Weight(
                            date_time=datetime.now(),
                            initial_weight=weight[1],
                            final_weight=weight[2],
                            package=package_obj,
                            scale=scale_obj))
        if len(data) > 0:
            print(f'{len(data)} Weights to write: ', *[i.to_dict() for i in data])
        session.add_all(data)
        session.commit()
        return update_packages
    except Exception as e:
        session.rollback()
        raise DBException("Error al escribir los pesos", e)


def write_http_weight(weights: HttpWeight, scale_obj: Scale):
    try:
        data = []
        time_last_weight = max([_.ts for _ in weights.pesos])
        for weight in weights.pesos:
            if weight.peso_final > 0:
                date_time = datetime.now() - timedelta(microseconds=(time_last_weight - weight.ts))
                package_obj = session.query(Package).filter(Package.package_id == weight.paquete).first()
                data.append(Weight(
                    date_time=date_time,
                    initial_weight=weight.peso_inicial,
                    final_weight=weight.peso_final,
                    package=package_obj,
                    scale=scale_obj))

        print(f'{len(data)} Weights to write: ', *[i.to_dict() for i in data])
        session.add_all(data)
        session.commit()
    except Exception as e:
        print(f"Unexpected error occurred: {e}")
        raise Exception("Unexp  ected error while writing HTTP weights", e)
