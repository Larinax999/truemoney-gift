from httpx import Client
from random import shuffle
import ssl

class SSLFactory:
    def __init__(self):
        self.ciphers = 'ECDH+AESGCM:DH+AESGCM:ECDH+AES256:DH+AES256:ECDH+AES128:DH+AES:ECDH+HIGH:DH+HIGH:ECDH+3DES:DH+3DES:RSA+AESGCM:RSA+AES:RSA+HIGH:RSA+3DES'.split(":")
 
    def __call__(self) -> ssl.SSLContext:
        shuffle(self.ciphers)
        ciphers = ":".join(self.ciphers)
        ciphers = ciphers + ":!aNULL:!eNULL:!MD5"
        context = ssl.create_default_context()
        context.set_ciphers(ciphers)
        return context

sslgen = SSLFactory()
sess = Client(verify=sslgen(),headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36 Edg/92.0.902.67"})
def voucher(v:str,num:str):
    v = v.replace('/','').split('v=')[-1]
    if 18 != len(v): return {"succes": False,"msg":"INVAILD_VOUCHER"}
    o=sess.post(f'https://gift.truemoney.com/campaign/vouchers/{v}/redeem',json={"mobile":num,"voucher_hash":v}).json()
    if "SUCCESS" == o['status']['code'] :
        return{'succes': True, 'amount': int(float(o['data']['my_ticket']['amount_baht'].replace(",",""))),'owner_full_name': o['data']['owner_profile']['full_name'],'code': v}
    return {"succes": False,"msg":o['status']['code']}

if __name__ == "__main__":
    print(voucher("testtesttesttestte","0123456789"))
