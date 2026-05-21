from app.logs.logging_config import Logger
from app.models.package import Package
from app.schemas.scale import Scale
import requests
import json
from app.crud import scale


class HttpClient:

    _instance = None

    def __init__(self):
        self.logger = Logger("HttpScale-Services").logger
        self.logger.info("Initializing HttpScale")

    def load_packages(self, scale: Scale):
        self.logger.info(f"Loading packages for HTTP scale {scale.name if hasattr(scale, 'name') else scale}")
        upload_packages = [
            {
                "id": pkg.package_id,
                "peso_min": pkg.minimum_weight,
                "peso_max": pkg.maximum_weight
            }
            for pkg in scale.packages
        ]
        json_data = json.dumps(upload_packages)
        url = f"http://{scale.ip}/modify_packages"
        try:
            response = requests.post(url, data=json_data, headers={"Content-Type": "application/json"}, timeout=10)
            response.raise_for_status()
            self.logger.info(f"Respuesta de {url}: {response.status_code} - {response.text}")
        except requests.exceptions.Timeout:
            print(f"Timeout al intentar conectar con {url}")
            self.logger.error(f"Timeout al intentar conectar con {url}")
        except requests.exceptions.ConnectionError:
            print(f"No se pudo conectar con {url}")
            self.logger.error(f"No se pudo conectar con {url}")
        except requests.exceptions.HTTPError as e:
            print(f"Error HTTP al conectar con {url}: {e}")
            self.logger.error(f"Error HTTP al conectar con {url}: {e}")
        except Exception as e:
            print(f"Error inesperado enviando paquetes a {url}: {e}")
            self.logger.error(f"Error inesperado enviando paquetes a {url}: {e}")

    def update_package(self, package: Package):
        try:
            scales = scale.read_all()
            for _scale in scales:
                try:
                    if any(package.package_id == p.package_id for p in _scale.packages):
                        if _scale.comunicacion == "HTTP":
                            self.load_packages(_scale)
                except Exception as e:
                    self.logger.error(f"Error procesando scale {getattr(scale, 'name', scale)}: {e}")
        except Exception as e:
            self.logger.error(f"Error general en update_package para package {package.package_id}: {e}")

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(HttpClient, cls).__new__(cls)
        return cls._instance


HttpScale = None
try:
    HttpScale = HttpClient()
except:
    pass