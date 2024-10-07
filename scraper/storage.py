from abc import ABC, abstractmethod
from typing import List
from models.product import Product
from sqlalchemy import create_engine, Column, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class ProductModel(Base):
    __tablename__ = 'products'
    product_title = Column(String, primary_key=True, index=True)
    product_price = Column(Float)
    path_to_image = Column(String)

class StorageInterface(ABC):
    @abstractmethod
    def save_products(self, products: List[Product]):
        pass

    @abstractmethod
    def update_product(self, product: Product):
        pass

class SQLiteStorage(StorageInterface):
    def __init__(self, db_path: str = "products.db"):
        self.engine = create_engine(f'sqlite:///{db_path}')
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def save_products(self, products: List[Product]):
        session = self.Session()
        for product in products:
            db_product = ProductModel(
                product_title=product.product_title,
                product_price=product.product_price,
                path_to_image=product.path_to_image
            )
            session.merge(db_product)  # merge to handle existing entries
        session.commit()
        session.close()

    def update_product(self, product: Product):
        session = self.Session()
        db_product = session.query(ProductModel).filter_by(product_title=product.product_title).first()
        if db_product:
            db_product.product_price = product.product_price
            db_product.path_to_image = product.path_to_image
        else:
            db_product = ProductModel(
                product_title=product.product_title,
                product_price=product.product_price,
                path_to_image=product.path_to_image
            )
            session.add(db_product)
        session.commit()
        session.close()