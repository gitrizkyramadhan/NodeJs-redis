from linebot.models import CarouselColumn
from linebot.models import CarouselTemplate
from linebot.models import MessageTemplateAction
from linebot.models import PostbackTemplateAction
from linebot.models import TemplateSendMessage
from linebot.models import URITemplateAction

carousels = [{
"id" : "greetings",
    "payload" : TemplateSendMessage(
        alt_text='Greetings',
        template=CarouselTemplate(
            columns=[
                CarouselColumn(
                    thumbnail_image_url='https://bangjoni.com/images/bni/BNI-Carousel-Menu_Produk.jpg',
                    title='PRODUK',
                    text='Info Produk',
                    actions=[
                        MessageTemplateAction(
                            label='Info Produk',
                            text='info produk'
                        )
                    ]
                 ),
                CarouselColumn(
                    thumbnail_image_url='https://bangjoni.com/images/bni/BNI-Carousel-Menu_Promo.jpg',
                    title='PROMO',
                    text='Info Promo',
                    actions=[
                        MessageTemplateAction(
                            label='Promo',
                            text='info promo'
                        )
                    ]
                ),
                CarouselColumn(
                    thumbnail_image_url='https://bangjoni.com/images/bni/BNI-Carousel-Menu_ATM.jpg',
                    title='ATM',
                    text='Info ATM',
                    actions=[
                        MessageTemplateAction(
                            label='Info Lokasi ATM',
                            text='info atm'
                        )
                    ]
                ),
                CarouselColumn(
                    thumbnail_image_url='https://bangjoni.com/images/bni/BNI-Carousel-Menu_Branch.jpg',
                    title='CABANG',
                    text='Info Cabang',
                    actions=[
                        MessageTemplateAction(
                            label='Info ',
                            text='info cabang'
                        )
                    ]
                ),
                CarouselColumn(
                    thumbnail_image_url='https://bangjoni.com/images/bni/BNI-Carousel-Menu_Agen46_2.jpg',
                    title='AGEN46',
                    text='Info Agen46',
                    actions=[
                        MessageTemplateAction(
                            label='Info Agen46',
                            text='info agen'
                        )
                    ]
                )

            ]
        )
    )
},{
"id" : "produk",
    "payload" : TemplateSendMessage(
        alt_text='Produk',
        template=CarouselTemplate(
            columns=[
                CarouselColumn(
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
            ]
        )
    )
},
    {
        "id": "promo_makanan",
        "payload": TemplateSendMessage(
            alt_text='Promo',
            template=CarouselTemplate(
                columns=[
                    CarouselColumn(
                        thumbnail_image_url='https://bangjoni.com/images/bni/Carousel-Menu_Food-Promo02.jpg',
                        title="Pringsewu Resto",
                        text="Diskon 20% di Pringsewu Group",
                        actions=[
                            PostbackTemplateAction(
                                label='Detail Info',
                                data='&evt=info_promo&detail_info=-Diskon 20% berlaku untuk transaksi pembelian food dan beverage (khusus menu ala carte).\n- Minimal transaksi Rp 200.000 berlaku di Resto Pringsewu.\n- Minimal transaksi Rp 100.000 berlaku di Mie Pasar Baru dan RM Kabayan.\n- Tidak berlaku kelipatan dan split transaksi dan hanya berlaku untuk dine in dan delivery.\n- Promo berlaku untuk semua jenis Kartu Kredit BNI kecuali Corporate Card dan Hasanah Card.\n- Berlaku di semua resto Pringsewu Group.'
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://bangjoni.com/images/bni/Carousel-Menu_Food-Promo01.jpg',
                        title="CFC",
                        text="Free Ayam setiap Senin dan Free Upsize di hari lain dengan Kartu Debit BNI di CFC",
                        actions=[
                            PostbackTemplateAction(
                                label='Detail Info',
                                data='&evt=info_promo&detail_info=Syarat dan Ketentuan:\n\n- Free Ayam setiap Senin untuk transaksi minimal Rp 50 ribu.\n- Maksimum free ayam 2 pcs.\n- Free upsize untuk pembelian Paket  Astaga setiap Selasa - Minggu.\n- maksimum 4 paket yang akan mendapatkan free upsize.\n- Berlaku untuk Kartu Debit BNI berlogo MasterCard kecuali BNI Debit Syariah.\n- Berlaku hingga 30 November 2017.'
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://bangjoni.com/images/bni/Carousel-Menu_Food-Promo03.jpg',
                        title="BAKMI GM",
                        text="Diskon 20% di Pringsewu Group",
                        actions=[
                            PostbackTemplateAction(
                                label='Detail Info',
                                data='&evt=info_promo&detail_info=-Gratis Pangsit Goreng isi 5 dengan minimum transaksi  Rp 125.000,- (sebelum pajak).\n- Berlaku untuk semua Kartu Debit BNI berlogo MasterCard, kecuali Kartu Debit BNI Syariah.\n- Berlaku di seluruh outlet Bakmi GM di seluruh Indonesia, kecuali Store Bandara dan Stasiun.\n- Berlaku untuk santap di tempat (dine in).\n- Promo berlaku hingga 31 Agustus 2017'
                            )
                        ]
                    )
                ]
            )
        )
    },
{
        "id": "promo_gadget",
        "payload": TemplateSendMessage(
            alt_text='Promo Gadget',
            template=CarouselTemplate(
                columns=[
                    CarouselColumn(
                        thumbnail_image_url='https://bangjoni.com/images/bni/Carousel-Menu_Gadget-Promo01.jpg',
                        title="ERAFONE",
                        text="Cashback hingga Rp 500 ribu + Cicilan 0% di PRJ 2017 dengan Kartu Kredit BNI",
                        actions=[
                            PostbackTemplateAction(
                                label='Detail Info',
                                data='&evt=info_promo&detail_info=Mekanisme :\n- Cashback Rp 200 ribu setiap transaksi minimal Rp 3.000.000,- untuk 60 orang pertama dengan menggunakan Kartu Kredit BNI.\n- Cashback Rp 300 ribu setiap transaksi minimal Rp 5.000.000,- untuk 50 orang pertama dengan menggunakan Kartu Kredit BNI.\n- Cashback Rp 500 ribu setiap transaksi minimal Rp 10.000.000,- untuk 40 orang pertama dengan menggunakan Kartu Kredit BNI.\n- Cashback digabungkan program BNI Installment 0 persen tenor sd 24 bulan langsung di EDC BNI.'
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://bangjoni.com/images/bni/Carousel-Menu_Gadget-Promo02.jpg',
                        title="ERAFONE",
                        text="Diskon 100 Ribu di Erafone.com dengan Kartu Kredit BNI",
                        actions=[
                            PostbackTemplateAction(
                                label='Detail Info',
                                data='&evt=info_promo&detail_info=Syarat dan Ketentuan:\n- Diskon Rp 100 ribu untuk 15 transaksi pertama di setiap hari Senin dengan minimum transaksi Rp 1,5 juta dengan menggunakan Kartu Kredit BNI.\n- Diskon langsung memotong harga produk.\n- Berlaku setiap hari Senin hingga tanggal 25 Desember 2017.\n- Berlaku untuk semua jenis Kartu Kredit BNI kecuali Corporate Card, BNI-JCB dan iB Hasanah Card.\n- Pembelian dilakukan di Erafone.com\n- Diskon wajib digabungkan dengan cicilan 0% hingga 12 bulan langsung di IPG BNI.\n- Pembelian dibatasi maksimal 1 kuota diskon untuk 1 pemegang kartu setiap hari Senin.'
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://bangjoni.com/images/bni/Carousel-Menu_Gadget-Promo03.jpg',
                        title="Beli Samsung dapat Samsung di Best N Cheap - Pekanbaru",
                        text="Diskon 20% di Pringsewu Group",
                        actions=[
                            PostbackTemplateAction(
                                label='Detail Info',
                                data='&evt=info_promo&detail_info=1. Menangkan hadiah langsung dengan minimal transaksi Rp 2,5 juta khusus pengguna Kartu Kredit BNI :\n- Galaxy A7 2017 1 (satu) unit\n- Galaxy A5 2017 1 (satu) unit\n- Samsung J2 Prime 3 (tiga) unit\n- Samsung Lipat 1272 12 (dua belas) unit\n- dan hadiah menarik lainnya\n\n2. Hemat hingga 50% dengan Redeem Point atau maksimal redeem Rp.1.000.000,-  (1 point = Rp.5,-)\n\n3. Berlaku cicilan 0% tenor 6&12 bulan\n\n4. Berlaku untuk seluruh jenis Kartu Kredit BNI kecuali iB Hasanah card dan Corporate card\n\n5. Berlaku setiap hari selama periode program termasuk hari libur Nasional dan Lokal\n\n6. Syarat dan Ketentuan berlaku.'
                            )
                        ]
                    )
                ]
            )
        )
    }
]

def composeCarousel(alt_text, columns):
    carousel_columns = []
    for column in columns:
        actions = []
        for action in column['actions']:
            if action['type'] == 'postback':
                actions.append(PostbackTemplateAction(label=action['label'], data=action['data']))
            elif action['type'] == 'message':
                actions.append(MessageTemplateAction(label=action['label'], text=action['text']))
            elif action['type'] == 'uri':
                actions.append(URITemplateAction(label=action['label'], uri=action['uri']))
        col = CarouselColumn(thumbnail_image_url=column['thumbnail_image_url'], title=column['title'], text=column['text'], actions=actions)
        carousel_columns.append(col)
    template = TemplateSendMessage(alt_text=alt_text, template=CarouselTemplate(columns=carousel_columns))
    print template
    return template