from pydantic import AnyHttpUrl,BaseModel,field_validator
from typing import Optional
import validators

class UrlIn(BaseModel):
    url:AnyHttpUrl
    custom_alias:Optional[int]=None
    expires_in_days:Optional[int]=None
    field_validator('url')
    @classmethod
    def validate_url(cls,v):
        url_str=str(v)
        if len(url_str)>2000:
            raise ValueError('Url is too long')

        suspicious_patttern=['javascript:','data:','vbscript:']
        for pattern in suspicious_patttern:
            if pattern in url_str:
                raise ValueError('Invalid Url: suspicious pattern detected !')
        return v
    field_validator('custom_alias')
    @classmethod
    def validate_alias(clas,v):
        if v is None:
            return v
        if not v.replace('-','').replace('_','').isalnum():
            raise ValueError('Alias must be betwwen 3 and 20 charater')
        return v
    field_validator('expire_in_days')
    @classmethod
    def validate_expiry(clas,v):
        if v is None:
            return v
        if v<1:
            raise ValueError("Expiration must be atleast 1 day")
        if v >365:
            raise ValueError('Maximum expiration must be 365 day')
        return v


