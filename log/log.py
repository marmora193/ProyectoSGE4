import logging

logging.basicConfig(
    filename="actividad.log",
    level=logging.INFO,
    format="%(asctime)s - %(message)s"
)

def registrar(mensaje):
    logging.info(mensaje)