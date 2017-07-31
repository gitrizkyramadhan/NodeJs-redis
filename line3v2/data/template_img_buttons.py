from linebot.models import ButtonsTemplate
from linebot.models import MessageTemplateAction
from linebot.models import PostbackTemplateAction
from linebot.models import TemplateSendMessage
from linebot.models import URITemplateAction

imgbuttons = [{
    "id":"example",
    "payload": TemplateSendMessage(
        alt_text='Buttons template',
        template=ButtonsTemplate(
            thumbnail_image_url='https://example.com/image.jpg',
            title='Menu',
            text='Please select',
            actions=[
                PostbackTemplateAction(
                    label='postback',
                    text='postback text',
                    data='action=buy&itemid=1'
                ),
                MessageTemplateAction(
                    label='message',
                    text='message text'
                ),
                URITemplateAction(
                    label='uri',
                    uri='http://example.com/'
                )
            ]
        )
    )
},{
    "id":"bjpay_register",
    "payload": TemplateSendMessage(
        alt_text='Register BJPAY',
        template=ButtonsTemplate(
            thumbnail_image_url='https://bangjoni.com/v2/carousel/greetings/bjpay.png',
            title='Register BJPAY',
            text='Buat BJPAY biar kamu gampang transaksinya',
            actions=[
                MessageTemplateAction(
                    label='Register',
                    text='bjpay register'
                )
            ]
        )
    )
},{
    "id":"uber_after_auth",
    "payload": TemplateSendMessage(
        alt_text='Uber',
        template=ButtonsTemplate(
            thumbnail_image_url='https://bangjoni.com/v2/carousel/images/uber.png',
            title='Pesen Uber',
            text='Account Uber kamu udah terhubung',
            actions=[
                MessageTemplateAction(
                    label='Lanjut Pesen',
                    text='uber'
                )
            ]
        )
    )
},
{
    "id":"produk",
    "payload": TemplateSendMessage(
        alt_text='Produk',
        template=ButtonsTemplate(
            thumbnail_image_url='https://bangjoni.com/images/bni/BNI-Carousel-Menu_Produk.jpg',
            title="INFO PRODUK",
            text="Info Produk",
            actions=[
                PostbackTemplateAction(
                    label='SIMPANAN',
                    data='&evt=produk&subevt=simpanan'
                ),
                PostbackTemplateAction(
                    label='KARTU KREDIT',
                    data='&evt=produk&subevt=kredit'
                ),
                PostbackTemplateAction(
                    label='PINJAMAN',
                    data='&evt=produk&subevt=pinjaman'
                ),
            ]
        )
    )
},
{
    "id":"promo",
    "payload": TemplateSendMessage(
        alt_text='Promo',
        template=ButtonsTemplate(
                        thumbnail_image_url='https://bangjoni.com/images/bni/BNI-Carousel-Menu_Promo.jpg',
                        title="INFO PROMO",
                        text="Info Promo",
                        actions=[
                            PostbackTemplateAction(
                                label='MAKANAN',
                                data='&evt=promo&subevt=makanan'
                            ),
                            PostbackTemplateAction(
                                label='GADGET',
                                data='&evt=promo&subevt=gadget'
                            ),
                            URITemplateAction(
                                label='LAINNYA',
                                uri='https://m.bnizona.com/index.php/category/index/promo'
                            ),
                        ]
        )
    )
}
]

def compose_img_buttons(alt_text, thumbnail_url, title, description, actions):
    img_actions = []
    for action in actions :
        if action['type'] == 'postback':
            img_actions.append(PostbackTemplateAction(label=action['label'], data=action['data']))
        elif action['type'] == 'message':
            img_actions.append(MessageTemplateAction(label=action['label'], text=action['text']))
        elif action['type'] == 'uri':
            img_actions.append(URITemplateAction(label=action['label'], uri=action['uri']))
    return TemplateSendMessage(
        alt_text=alt_text,
        template=ButtonsTemplate(
            thumbnail_image_url=thumbnail_url,
            title=title,
            text=description,
            actions=img_actions
        ))