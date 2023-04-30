from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import (
    declarative_base,
    relationship,
    backref,
    sessionmaker
)
from sqlalchemy import (
    Column,
    ForeignKey,
    PrimaryKeyConstraint,
    CheckConstraint,
    ForeignKeyConstraint,
)
from sqlalchemy import (
    String,
    Integer,
    Numeric,
    DateTime,
    Boolean,
)

Base = declarative_base()

class Cookie(Base):
    __tablename__ = 'cookie_orm'
    
    cookie_id = Column(Integer(), primary_key=True)
    cookie_name = Column(String(50), index=True)
    cookie_recipe_url = Column(String(255))
    cookie_sku = Column(String(55))
    quantity = Column(Integer())
    unit_cost = Column(Numeric(12, 2))

    def repr(self):
        return (
            f"Cookie(\
                cookie_id='{self.cookie_id}', \
                cookie_name='{self.cookie_name}', \
                cookie_recipe_url='{self.cookie_recipe_url}', \
                cookie_sku='{self.cookie_sku}', \
                quantity='{self.quantity}', \
                unit_cost='{self.unit_cost}' \
                )"
        )

class User(Base):
    __tablename__ = 'user_orm'
    
    user_id = Column(Integer(), primary_key=True)
    username = Column(String(15), nullable=False, unique=True)
    email_address = Column(String(255), nullable=False)
    phone = Column(String(20))
    password = Column(String(25), nullable=False)
    created_on = Column(DateTime(), default=datetime.now)
    updated_on = Column(DateTime(), default=datetime.now, onupdate=datetime.now)
    
# 制約の追加
class SomeData(Base):
    __tablename__ = 'somedatatable_orm'
    __table_args__ = (
        ForeignKeyConstraint(['id'], ['user_orm.user_id']),
        CheckConstraint('unit_cost >= 0.00', name='unit_cost_positive'),
    )
    
    id = Column(Integer(), primary_key=True)
    unit_cost = Column(Numeric(12, 2))
    
# リレーション(一対多)
class Order(Base):
    __tablename__ = 'order_orm'
    order_id = Column(Integer(), primary_key=True)
    user_id = Column(Integer(), ForeignKey('user_orm.user_id'))
    shipped = Column(Boolean(), default=False)
    
    user = relationship('User', backref=backref('order_orm', order_by=order_id))

# リレーション(一対一)
class LineItem(Base):
    __tablename__ = 'line_items_orm'
    
    line_item_id = Column(Integer(), primary_key=True)
    order_id = Column(Integer(), ForeignKey('order_orm.order_id'))
    cookie_id = Column(Integer(), ForeignKey('cookie_orm.cookie_id'))
    quantity = Column(Integer())
    expanded_cost = Column(Numeric(12, 2))
    
    order = relationship('Order', backref=backref('line_items', order_by=line_item_id)) # 一対多
    cookie = relationship('Cookie', uselist=False) # 一対一

    
def create_all(engine):
    Base.metadata.create_all(engine)

if __name__ == '__main__':
    engine = create_engine('postgresql+pg8000://postgres:password@localhost:5432/test', echo=True) # postgresql
    # create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    cookie = Cookie(
        cookie_name='chocolate chip',
        cookie_recipe_url='http://hoge.com/hoge.html',
        cookie_sku='CCO1',
        quantity='12',
        unit_cost='0.50'
    )
    session.add(cookie)
    session.flush() # commitせずに内容を確認
    # session.commit()
