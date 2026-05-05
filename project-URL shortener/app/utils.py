import secrets
import string
from datetime import datetime,timedelta
from fastapi import HTTPException
def generate_key(length=5):
    alphabet=string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))
def base62_encode(num):
    alphabet = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    if num == 0:
        return alphabet[0]
    result = ''
    while num > 0:
        num, remainder = divmod(num, 62)
        result = alphabet[remainder] + result
    return result
def base62_decode(s):
    alphabet = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    num = 0
    for char in s:
        num = num * 62 + alphabet.index(char)
    return num

def encode(num):
    aplhabet="0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    if num==0:
        return aplhabet[0]
    res=''
    while num>0:
        idx=num%62
        res=aplhabet[idx]+res
        num=num//62
    return res
def decode(num):
    idx=0
    mapp={}
    alphabet="0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    while idx<62:
        mapp[alphabet[idx]]=idx
        idx+=1
    result=0
    idx=0
    while idx<len(num):
        result+=62*result+mapp[num[idx]]
        idx+=1
    return result


# cnt:dict[str:int]={}
# def rate_limiting(request,window_size,max_count=20):
#     client_ip=request.client.host
#     now=datetime.now()
#     end=now+timedelta(minutes=window_size)
#     if client_ip not in cnt:
#         cnt[client_ip]={"cnt":1,"reset_at":end}
#         return
#     if cnt[client_ip]['reset_at']<end:
#         cnt[client_ip]['reset_at']=end
#         cnt[client_ip]["cnt"]=1
#         return 
#     cnt[client_ip]["cnt"]+=1
#     if cnt[client_ip]["cnt"]>max_count:
#         raise HTTPException(
#             status_code=429,
#             detail={
#                 "error": "RATE_LIMIT_EXCEEDED",
#                 "message": f"Too many requests. Max {max_requests} per {window_minutes} minute(s)",
#                 "reset_at": ip_data["reset_at"].isoformat()
#             }
#         )
cnt = {}

def rate_limiting(request, window_size, max_count=30):
    client_ip = request.client.host
    now = datetime.now()

    if client_ip not in cnt:
        cnt[client_ip] = {
            "cnt": 1,
            "reset_at": now + timedelta(minutes=window_size)
        }
        return

    ip_data = cnt[client_ip]

    if now > ip_data["reset_at"]:
        ip_data["cnt"] = 1
        ip_data["reset_at"] = now + timedelta(minutes=window_size)
        return

    ip_data["cnt"] += 1

    if ip_data["cnt"] > max_count:
        raise HTTPException(status_code=429, detail="Rate limit exceeded")