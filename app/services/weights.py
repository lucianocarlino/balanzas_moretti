from app.crud import scale
from app.db.base import session
from app.services.modbusMaster import Master
from app.crud.weight import write_weight
import pandas as pd

class Weights:
    def __init__(self):
        self.scales = scale.read_all()

    async def read_weights_from_scales(self):
        weights = []
        for scale in self.scales:
            weights_from_scale = Master.read_weights_from_scale(scale)
            if weights_from_scale == None or len(weights_from_scale) == 0:
                scale.online = False
                pass
            else:
                if scale.online == False:
                    scale.online = True
                    Master.load_packages(scale.slave_address, scale.packages)
                print(f"Scale {scale.name} is online. Weights: {weights_from_scale}")
                weights.append(weights_from_scale)
        write_weight(weights)
        return weights
    
    def refresh_scales(self):
        self.scales = scale.read_all()
    
weights = Weights()
            
def generate_csv(weights : list[Weights]):
    weights_data = [weight.to_dict() for weight in weights]
    df = pd.DataFrame(weights_data)
    df.to_csv("weights.csv", index=False)

