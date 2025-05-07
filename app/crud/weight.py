from datetime import datetime
from sqlalchemy import DateTime
from app.models.weight import Weight
from app.models.package import Package
from app.models.scale import Scale
from app.db.base import session

def read_all(limit: int, init: DateTime = None, end: DateTime = None, package_id: int = None, scale_id: int = None):
    
    query = session.query(Weight)

    if (init and end):
        query = query.filter(Weight.date_time >= init).filter(Weight.date_time <= end)

    if package_id:
        query = query.filter(Weight.package_id == package_id)

    if scale_id:
        query = query.filter(Weight.scale_id == scale_id)   

    return query.limit(limit).all()

def write_weight(weights):
    data = []
    for scale in weights:
        if scale == []:
            continue
        scale_id = scale[0]
        scale.pop(0)
        for weight in scale[:-1]:
            if weight[0] > 0:
                package = session.query(Package).filter(Package.package_id == weight[0]).first()
                scale = session.query(Scale).filter(Scale.scale_id == scale_id).first()
                data.append(Weight(
                date_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 
                initial_weight=weight[1], 
                final_weight=weight[2], 
                package=package,
                scale=scale))
    print(f"Weights to write: {data}")
    session.add_all(data)
    session.commit()

