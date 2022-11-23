from model.image import Image
from database.connection import Session


class ImageController:


    @staticmethod
    def insert(name, latitude, longitude):
        result = False
        image = Image(name, latitude, longitude)
        session = Session()
        try:
            session.add(image)
            session.commit()
            result = True
        except Exception as e:
            print(f"Error: {e}")
        finally:
            session.close()

        return result

    
    @staticmethod
    def read_all():
        result = False
        session = Session()
        try:
            result = session.query(Image).all()
        except Exception as e:
            print(f"Error: {e}")
        finally:
            session.close()

        return result

        
    