from app.crud import scale
from app.schemas.scale import Scale as schemaScale, ScaleCreate, ScaleUpdate
from app.models.scale import Scale
from app.models.scales_has_packages import ScaleHasPackages
from app.models.weight import Weight
from app.models.package import Package
from datetime import datetime, timedelta
from sqlalchemy import DateTime
from app.models.weight import Weight
from app.models.package import Package
from app.models.scale import Scale
from app.db.base import session
import random



def generate_random_weights():
    data = []
    i = 0
    day = datetime.now().replace(year=2025, month=12, day=8)
    scales = scale.read_all()
    while i < 32:
        for scl in scales:
            boxs = random.randint(1, 50)
            pkg = scl.packages[random.randint(0, len(scl.packages) - 1)]
            for box in range(boxs):
                if (random.random() > 0.9):
                    pkg = scl.packages[random.randint(0, len(scl.packages) - 1)]
                initial_weight = random.uniform(pkg.minimum_weight - pkg.minimum_weight * 0.25, pkg.maximum_weight + pkg.maximum_weight * 0.25)
                if pkg.maximum_weight > initial_weight > pkg.minimum_weight:
                    final_weight = initial_weight
                else:
                    final_weight = pkg.minimum_weight + random.random() * (pkg.maximum_weight - pkg.minimum_weight)
            weight = Weight(
                date_time=day.strftime("%Y-%m-%d %H:%M:%S"),
                initial_weight=round(initial_weight, 2),
                final_weight=round(final_weight, 2),
                package=pkg,
                scale=scl
            )
            data.append(weight)
        i += 1
        day += timedelta(days=1)
    session.add_all(data)
    session.commit()

generate_random_weights()