from slacker import Slacker

slack = Slacker('xoxb-3406314155365-3433339692400-R5cTypQNNwvuZodBILiljefB')

markdown_text = '''
This message is plain.
*This message is bold.*
`This message is code.`
_This message is italic._
~This message is strike.~
'''

attach_dict = {
    'color': '#ff0000',
    'author_name': 'dyun-finance',
    'title': '오늘의 증시 KOSPI',
    'title_link': 'http://finance.naver.com/sise/sise_index.nhn?code=KOSPI',
    'image_url': 'http://ssl.pstatic.net/imgstock/chart3/day/KOSPI.png'
}

attach_list = [attach_dict]
slack.chat.post_message(channel="general", text=markdown_text, attachments=attach_list)
