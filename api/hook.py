from sqlalchemy import exists
from models import Cookie,engine
from sqlalchemy.orm import sessionmaker

orm_session = sessionmaker(engine)()

def request(flow):
    request = flow.request
    print("request.url ====> ",request.url)
    print("cookies ====> ",dict(request.cookies))
    dcookies = dict(request.cookies)
    if "devicefinger" in str(dict(request.cookies)):
        pin_exists = orm_session.query(exists().where(Cookie.pin==dcookies.get("pin"))).scalar()
        if not pin_exists:
            orm_session.add(Cookie(pin=dcookies.get("pin"),
                wskey=dcookies.get("wskey"),
                whwswswws=dcookies.get("whwswswws"),
                unionwsws=dcookies.get("unionwsws"),
                url=request.url))
            orm_session.commit()