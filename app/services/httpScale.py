import time

from app.logs.logging_config import Logger
from app.models.package import Package
from app.schemas.scale import Scale
from app.models.scale import Scale as ModelScale
import requests
import json
from app.crud import scale


class HttpClient:

    _instance = None

    def __init__(self):
        self.logger = Logger("HttpScale-Services").logger
        self.logger.info("Initializing HttpScale")

    def load_packages(self, scale: ModelScale):
        retries = 0
        timeout = False
        connerror = False
        httperror = False
        unexpected = [False,""]
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
        while retries < 3:
            try:
                response = requests.post(url, data=json_data, headers={"Content-Type": "application/json"}, timeout=5)
                response.raise_for_status()
                self.logger.info(f"Respuesta de {url}: {response.status_code} - {response.text}")
            except requests.exceptions.Timeout:
                print(f"Timeout al intentar conectar con {url}")
                timeout = True
            except requests.exceptions.ConnectionError:
                print(f"No se pudo conectar con {url}")
                connerror = True
            except requests.exceptions.HTTPError as e:
                print(f"Error HTTP al conectar con {url}: {e}")
                httperror = True
            except Exception as e:
                print(f"Error inesperado enviando paquetes a {url}: {e}")
                unexpected = [True, e]
            retries += 1
            time.sleep(2)
        if timeout:
            self.logger.error(f"Error de timeout al enviar paquetes a {url} después de 3 intentos")
        if connerror:
            self.logger.error(f"Error al conectar con {url}")
        if httperror:
            self.logger.error(f"Error al conectar con {url}")
        if unexpected[0]:
            self.logger.error(f"Error inesperado enviando paquetes a {url}: {unexpected[1]}")

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

    def get_status(self, scale: ModelScale):
        url = f"http://{scale.ip}/status"
        try:
            response = requests.get(url, timeout=3)
            response.raise_for_status()
            return True
        except requests.exceptions.Timeout:
            print(f"Timeout al intentar conectar con {url}")
            self.logger.error(f"Timeout al intentar conectar con {url}")
            return None
        except requests.exceptions.ConnectionError:
            print(f"No se pudo conectar con {url}")
            self.logger.error(f"No se pudo conectar con {url}")
            return None
        except requests.exceptions.HTTPError as e:
            print(f"Error HTTP al conectar con {url}: {e}")
            self.logger.error(f"Error HTTP al conectar con {url}: {e}")
            return None
        except Exception as e:
            print(f"Error inesperado obteniendo status de {url}: {e}")
            self.logger.error(f"Error inesperado obteniendo status de {url}: {e}")
            return None

    def connect_scales(self):
        try:
            scales = scale.read_all()
            for _scale in scales:
                if _scale.comunicacion == "HTTP":
                    if self.get_status(_scale):
                        _scale.online = True
                        self.load_packages(_scale)
                        self.logger.info(f"Conexión exitosa con HTTP scale {getattr(_scale, 'name', _scale)}")
                    else:
                        _scale.online = False
                        self.logger.warning(f"HTTP scale {getattr(_scale, 'name', _scale)} desconectada")
        except Exception as e:
            self.logger.error(f"Error general en connect_scales: {e}")

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(HttpClient, cls).__new__(cls)
        return cls._instance


HttpScale = None
try:
    HttpScale = HttpClient()
except:
    pass