
from slacker import Slacker

slack = Slacker('xoxb-1472760183958-1479779745491-8x9UiIVNpIJ50RT9WUVYpDre')

markdown_text = '''
This message is plain.
*This message is bold.*
`This message is code.`
_This message is italic._
~This message is strike.~
'''


    
attach_dict = {
    'color'      :'#ff0000',
    'author_name':'Recog',
    'title'      :'오늘의 증시 KOSPI',
    'title_link' :'http://finance.naver.com/sise/sise_index.nhn?code=KOSPI',
    'text_url'   : '2414.79',
    'image_url'  :'https://ssl.pstatic.net/imgstock/chart3/day/KOSPI.png'
}

attach_list = [attach_dict]
slack.chat.post_message(channel="#invester", text=markdown_text, attachments=attach_list)
