from models import Base

from config import engine


def crear_tablas():
    Base.metadata.create_all(bind=engine)
    print("Tablas creadas correctamente en la bd 'oro'.")
if __name__ == '__main__':

    crear_tablas()
