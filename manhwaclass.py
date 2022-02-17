from sqlalchemy import true


class stateManhwa():
   
    switch=0
    buffer=0
    buffercancelsub=0
    buffmas=[]
    search=0
    chat=0
    bR='бвгд'
    txt=[]
    ManhwaSender=0
    payfullChapters=[0,0,0,0,0,0,6888,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]


def is_number(_str):
    try:
        int(_str)
        return True
    except ValueError:
        return False