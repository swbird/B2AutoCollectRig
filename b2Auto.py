import time
import os
import requests
from loguru import logger
logger.add('b2log.txt',encoding='utf-8')
def loadAuths():
    if os.path.exists('Authlist.txt'):
        pass
    else:
        with open('Authlist.txt', 'w', encoding='utf-8') as w:
            w.write('# 备注----合成类型----AuthToken\n')
            logger.info(f'Authlist.txt创建成功')
    filename = 'Authlist.txt'
    with open(filename, encoding='utf-8') as f:
        lines = [i for i in f.readlines() if '#' not in i]
    tmp = [i.replace(' ', '').replace('\n', '')
            for i in lines if i != '\n']
    return [i.split('----') for i in tmp]
class B2Auto():
    def __init__(self, authInfo:list):
        authorization = authInfo[2]
        name = authInfo[0]
        _type = authInfo[1]
        self.authorization = authorization
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
            'authorization':   self.authorization,
            'content-type': 'application/json'
        }
        self.session = requests.Session()
        self.session.headers = self.headers
        self.name = name
        self.type = _type
    def getRates(self):
        resp = self.session.get('https://buzz-api.bsquared.network/api/team/rates?')

        # print(resp.json())
        if resp.json()['message']=='success':
            parts = resp.json()['data']['parts']
            self_rate = resp.json()['data']['self_rate']
            addtion_rate = resp.json()['data']['addtion_rate']
            return parts, float(self_rate)+float(addtion_rate)

    def getRigs(self, ):
        resp = self.session.get('https://buzz-api.bsquared.network/api/rigs?')
        if resp.json()['message'] == 'success':
            data = resp.json()['data']
            print(data)
            return data

    def collectRig(self):
        if self.type == 'BASIC':
            params = {"parts_amount": 10, "assemble_spec": "one"}
            resp = self.session.post('https://buzz-api.bsquared.network/api/rigs/assemble/cpu', json=params)
            success = resp.json()['message']
            if success == 'success':
                logger.debug(f'{self.name} 领取BASIC矿机成功')
                return True
            return False
        else: # todo 等待更新 ADVANCED
            pass
if __name__ == '__main__':
    auths = loadAuths()
    print(f'读取到 {len(auths)} 个账号')
    while True:
        for auth in auths:
            b2 = B2Auto(auth)
            try:
                parts, rate = b2.getRates()
                logger.debug(f'{auth[0]}----parts:{parts}----rate:{rate}')
                if parts >= 10:
                    if b2.collectRig():
                        pass


            except Exception as e:
                logger.debug(f'{auth[0]} 查询失败e=>{e}')
                time.sleep(10) #
        time.sleep(100)  # 100s检查一次

