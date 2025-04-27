import requests
from fake_useragent import UserAgent
import re
#提取文件中的url
i=0
m=0
urls=[]
urld="https://weixin.sogou.com/weixin?ie=utf8&s_from=input&_sug_=n&_sug_type_=1&type=2&query=%E6%9D%80%E6%89%8B%E4%BB%A3%E5%8F%B747&w=01015002&oq=&ri=0&sourceid=sugg&sut=0&sst0=1744339582079&lkt=0%2C0%2C0&p=40040108"
with open('links.txt','r',encoding='utf-8') as links:
    for line in links:
        urls.append(line.strip())

#准备访问的条件
cookies = {
    "ABTEST": "0|1744356714|v1",
    "SUID": "AF5AD4DEC852A20B0000000067F8C56A",
    "SNUID": "62971A10CEC8FCB67C831EB5CECC3ED6"
}
ua=UserAgent()
header= ua.random
headers={"User-Agent": header}
#访问
with open('url.txt', 'w', encoding='utf-8') as file:
    for url in urls:
        res = requests.post(url=url,headers=headers,cookies=cookies)
        parts = []
        rule =  re.compile(r"url\s*=\s*'([^']*)'|url\s*\+=\s*'([^']*)'", re.IGNORECASE)
        pis = rule.findall(res.text)
        for pi in pis:
            for part in pi:
                if part:
                    parts.append(part)
        final = ''.join(parts)
        file.write(final+'\n')
        i=i+1
        m=m+1
        if i==10:
            response = requests.get(urld, headers=headers)
            cookies = response.cookies
            i=0
        print(f"已爬取{m}篇文章")
        print(final)