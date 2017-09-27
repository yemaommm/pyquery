# -*- coding: utf-8 -* 


'''{"expires_in":2592000,"refresh_token":"22.bfb57ea29936fa999f695b8c3cf395ce.315360000.1818058413.2872154778-10005038","access_token":"21.103d4bee70e7e8bf2d80f29d53aea958.2592000.1505290413.2872154778-10005038","session_secret":"b4e63b3edeeff2eb31f3fa656166b90f","session_key":"9mnRdanci4hUiFtORbbFPF+iZzT+UdosmAR\/gZRZaaoUC3zKvl1WHcPw6oujv7jfPJl40LONDMaz\/WC5RlNZOtCueRcvO7DXKTc=","scope":"basic netdisk"}'''


baiduapiurl = ''
redirect_uri = ''
access_token = '21.466ac3fdd9bda4a14e1fb8f4aed7c82e.2592000.1505293944.470523782-1685522'
refresh_token = '22.4d26f7ad5777bee4955186623a688675.315360000.1818061944.470523782-1685522'
ID = '1685522'
APIKey = 'PDVV6UdAxQ691Z24hSBwz8jy'
SecretKey = 'boM29ANsoKC3norwF7weNwyZHPyyAwUw'
codeurl = 'https://openapi.baidu.com/oauth/2.0/authorize?response_type=code&client_id=PDVV6UdAxQ691Z24hSBwz8jy&redirect_uri=oob&scope=basic+netdisk';
gactokenurl = 'https://openapi.baidu.com/oauth/2.0/token?grant_type=authorization_code&code=92b91d6587b79715b14e8b93484a17cd&client_id=PDVV6UdAxQ691Z24hSBwz8jy&client_secret=boM29ANsoKC3norwF7weNwyZHPyyAwUw&redirect_uri=oob&scope=basic+netdisk'

refresh_token_url = 'https://openapi.baidu.com/oauth/2.0/token?grant_type=refresh_token&refresh_token='+refresh_token+'&client_id='+APIKey+'&client_secret='+SecretKey+'&scope=basic+netdisk'