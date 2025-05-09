from app.db.base import Base, Meta, conn, engine, session
from app.models.scale import Scale
from app.models.weight import Weight
from app.models.package import Package
from app.models.scales_has_packages import ScaleHasPackages
from datetime import datetime


def migration():

    Base.metadata.create_all(engine)

    # test_package_1 = Package(name="package_test_1", expected_weight = -1, minimum_weight = -1.5, maximum_weight = -0.5, scales=[])
    # test_scale_1 = Scale(name="scale_test_1", packages=[test_package_1], mapped=True, online=False)
    # test_package_2 = Package(name="test_2", expected_weight = 100, minimum_weight = 95, maximum_weight = 105, scales=[])
    # test_scale_2 = Scale(name="scale_test_2", packages=[test_package_2], mapped=True, online=True)

    # session.add_all([test_scale_2, test_scale_1, test_package_2, test_package_1])
    # session.commit()

    # package_1 = session.query(Package).filter(Package.package_id == 1).first()
    # package_2 = session.query(Package).filter(Package.package_id == 2).first()
    # scale_1 = session.query(Scale).filter(Scale.scale_id == 1).first()
    # scale_2 = session.query(Scale).filter(Scale.scale_id == 2).first()

    # test_weight_1 = Weight(date_time=datetime.date(0), initial_weight=0.5, final_weight=1.5, package=package_1, scale=scale_1)
    # test_weight_2 = Weight(date_time=datetime.date(0), initial_weight=0.5, final_weight=1.5, package=package_1, scale=scale_2)
    # test_weight_3 = Weight(date_time=datetime.date(0), initial_weight=0.5, final_weight=1.5, package=package_2, scale=scale_1)
    # test_weight_4 = Weight(date_time=datetime.date(0), initial_weight=0.5, final_weight=1.5, package=package_2, scale=scale_2)

    # session.add_all([test_weight_1, test_weight_2, test_weight_3, test_weight_4])
    # session.commit()

migration()