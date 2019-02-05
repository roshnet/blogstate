import re


def validate_username(p):

    a=re.compile(r'^(?![-._])(?!.*[_.-]{2})[\w.-]{5,30}(?<![-._])$')
    
    if a.match(p) is None:
    	return 0
    else:
    	return 1	

def validate_email(q):
    
    b= re.compile(r"(?![-._])(?!.*[_.-]{2})[A-Za-z0-9-_.]+(?<![-._])@[A-Za-z0-9-]+(.[A-Za-z0-9]+)*(\.)([A-Za-z]{2,})")
    
    if b.match(q) is None:
    	return 0
    else:
    	return 1    	








    
