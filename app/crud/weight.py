from datetime import datetime
from sqlalchemy import DateTime
from app.models.weight import Weight
from app.models.package import Package
from app.models.scale import Scale
from app.db.base import session
from app.exceptions.DBException import DBException

def read_all(limit: int = 100000, init: DateTime = None, end: DateTime = None, package_id: int = None, scale_id: int = None):
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
                    data.append(Weight(
                    date_time=datetime.now(),
                    initial_weight=weight[1],
                    final_weight=weight[2],
                    package=package_obj,
                    scale=scale_obj))
        print("Weights to write: ", *[i.to_dict() for i in data])
        session.add_all(data)
        session.commit()
    except Exception as e:
        session.rollback()
        raise DBException("Error al escribir los pesos", e)
