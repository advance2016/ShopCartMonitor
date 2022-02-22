
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column,Integer,String
from hashlib import sha256
engine = create_engine('sqlite:///db/base.sqlite')
Base = declarative_base()

class ProductInfo(Base):
    __tablename__ = 'product_info'
    id = Column(Integer, primary_key=True, autoincrement=True)
    sku = Column(String)            # 产品sku
    name = Column(String)           # 产品名称
    stock_state = Column(String)    # 产品有无库存
    detail = Column(String)         # 产品详情链接
    min_price = Column(String)      # 购物车价格
    max_price = Column(String)      # 原生价格
    activate_info = Column(String)  # 优惠活动信息   
    fp = Column(String)             # sha256指纹

    def fingerprint(self):
        content = "{}-{}-{}-{}-{}-{}-{}".format(self.sku,
        self.name,self.stock_state,
        self.detail,self.min_price,
        self.max_price,self.activate_info).encode()
        return sha256(content).hexdigest()

    @classmethod
    def hash(cls,*args)->str:
        content = "{}-{}-{}-{}-{}-{}-{}".format(*args).encode()
        return sha256(content).hexdigest()

class Cookie(Base):
    __tablename__ = 'cookie'
    id = Column(Integer, primary_key=True, autoincrement=True)
    pin = Column(String)
    wskey = Column(String)
    whwswswws = Column(String)
    unionwsws = Column(String)
    url = Column(String)


    def compose_cookie(self):
        return 'pin={};wskey={};whwswswws={};unionwsws={};'.format(self.pin,self.wskey,self.whwswswws,self.unionwsws)


Base.metadata.create_all(engine)
