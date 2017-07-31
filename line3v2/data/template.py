

class Template:

    data_button_confirmation = [
        {
            "type": "postback",
            "title": "Ya",
            "payload": "&evt=iya_services"
        },
        {
            "type": "postback",
            "title": "Tidak",
            "payload": "&evt=tidak_services"
        }
    ]

    data_button_greeting = [
        {
            "type": "postback",
            "title": "Ya",
            "payload": "&evt=iya_greeting"
        },
        {
            "type": "postback",
            "title": "Tidak",
            "payload": "&evt=tidak_greeting"
        }
    ]

    data_template_greeting = [
               {
                "title":"PRODUK",
                "image_url":"https://bangjoni.com/images/bni/BNI-Carousel-Menu_Produk.jpg",
                "buttons":[
                  {
                    "type":"postback",
                    "title":"Info Produk",
                    "payload":"&evt=lihat_produk"
                  }
                ]
              },
              {
                "title":"PROMO",
                "image_url":"https://bangjoni.com/images/bni/BNI-Carousel-Menu_Promo.jpg",
                "buttons":[
                  {
                    "type":"postback",
                    "title":"Info Promo",
                    "payload":"&evt=lihat_promo"
                  }
                ]
              },
              {
                "title":"ATM",
                "image_url":"https://bangjoni.com/images/bni/BNI-Carousel-Menu_ATM.jpg",
                "buttons":[
                  {
                    "type":"postback",
                    "title":"Info ATM",
                    "payload":"&evt=lihat_atm"
                  }
                ]
              },
              {
                "title":"CABANG",
                "image_url":"https://bangjoni.com/images/bni/BNI-Carousel-Menu_Branch.jpg",
                "buttons":[
                  {
                    "type":"postback",
                    "title":"Info Cabang",
                    "payload":"&evt=lihat_cabang"
                  }
                ]
              },
            {
                "title": "AGEN46",
                "image_url": "https://bangjoni.com/images/bni/BNI-Carousel-Menu_Agen46_2.jpg",
                "buttons": [
                    {
                        "type": "postback",
                        "title": "Info Agen46",
                        "payload": "&evt=lihat_agen"
                    }
                ]
            }
            ]

    data_template_produk = [
        {
            "title": "INFO PRODUK",
            "image_url": "https://bangjoni.com/images/bni/BNI-Carousel-Menu_Produk.jpg",
            "buttons": [
                {
                    "type":"postback",
                    "title":"SIMPANAN",
                    "payload":"&evt=lihat_simpanan"
                },
                {
                    "type":"postback",
                    "title":"KARTU KREDIT",
                    "payload":"&evt=lihat_kartu_kredit"
                },
                {
                    "type":"postback",
                    "title":"PINJAMAN",
                    "payload":"&evt=lihat_pinjaman"
                }
            ]
        }
    ]

    data_template_promo = [
        {
            "title": "INFO PROMO",
            "image_url": "https://bangjoni.com/images/bni/BNI-Carousel-Menu_Promo.jpg",
            "buttons": [
                {
                    "type":"postback",
                    "title":"MAKANAN",
                    "payload":"&evt=info_makanan"
                },
                {
                    "type":"postback",
                    "title":"GADGET",
                    "payload":"&evt=info_gadget"
                },
                # {
                #     "type":"postback",
                #     "title":"FASHION",
                #     "payload":"&evt=info_fashion"
                # },
                {
                    "type": "web_url",
                    "title": "LAINYA",
                    "url": "https://m.bnizona.com/index.php/category/index/promo",
                    "webview_height_ratio": "compact"
                }
            ]
        }
    ]

    data_template_promo_fashion = [
        {
            "title": "Optik Tunggal",
            "subtitle" : "Special Price + Add. Discount 10% at Optik Tunggal",
            "image_url": "https://bangjoni.com/images/bni/Carousel-Menu_Fashion-Promo01.jpg",
            "buttons": [
                {
                    "type":"postback",
                    "title":"Detail Info",
                    "payload":"&evt=info_promo&detail_info=Mekanisme Promo:\n\n-Harga spesial untuk pembelian paket Frame dan Lensa dan Sunglasses. \n- Diskon tambahan 10% untuk pembelian frame menggunakan Kartu BNI.\n- Promo dapat digabungkan dengan program cicilan 0% 6 bulan untuk minimum transaksi Rp 1 juta atau hemat hingga 50% dengan menukarkan BNI Reward Points.\n- Program berlaku di seluruh outlet Optik Tunggal Indonesia.\n- Berlaku untuk semua jenis Kartu Kredit BNI (Visa, JCB dan MasterCard) kecuali iB Hasanah Card dan Corporate Card dan berlaku untuk semua jenis Kartu Debit BNI kecuali Debit Syariah."
                }
            ]
        },
        {
            "title": "Senayan City",
            "subtitle": "Ultimate Shopping Experience Starts from the Card",
            "image_url": "https://bangjoni.com/images/bni/Carousel-Menu_Fashion-Promo02.jpg",
            "buttons": [
                {
                    "type": "postback",
                    "title": "Detail Info",
                    "payload": "&evt=info_promo&detail_info=PROGRAM FREE VOUCHER\n- Free Shopping Voucher Senayan City 100 ribu dengan menukarkan struk belanja senilai minimal akumulasi transaksi Rp 1 juta.\n- Maksimal penggabungan 3 struk.\n- Berlaku kelipatan maksimal voucher 200 ribu.\n- Berlaku untuk 50 customer per hari.\n- Berlaku untuk semua transaksi di tenant apapun di Senayan City Mall.\n- Berlaku untuk semua jenis Kartu Kredit BNI.\n- Berlaku hingga 9 Juli 2017."
                }
            ]
        },
        {
            "title": "Shafira",
            "subtitle" : "Diskon hingga 25% di Shafira Group dengan Kartu Kredit BNI",
            "image_url": "https://bangjoni.com/images/bni/Carousel-Menu_Fashion-Promo03.jpg",
            "buttons": [
                {
                    "type": "postback",
                    "title": "Detail Info",
                    "payload": "&evt=info_promo&detail_info=Syarat dan Ketentuan:\n\n- Cicilan 0% 3 bulan, 6 bulan dan 12 bulan untuk minimum transaksi Rp 500 Ribu.\n- Diskon 25% untuk produk Shafira.\n- Diskon 15% untuk produk Zoya, Mezora & Encyclo.\n- Berlaku untuk semua jenis Kartu Kredit BNI kecuali Corporate Card.\n- Berlaku diseluruh butik Shafira, Zoya, Mezora & Encyclo.\n- Berlaku hingga 31 Desember 2017."
                }
            ]
        }#,
        # {
        #     "title": "Matahari",
        #     "subtitle": "Diskon hingga 25% di Shafira Group dengan Kartu Kredit BNI",
        #     "image_url": "https://m.bnizona.com//files/ed4956104103091a6f1a0a4080ee4e26.jpg",
        #     "buttons": [
        #         {
        #             "type": "postback",
        #             "title": "Detail Info",
        #             "payload": "&evt=info_promo&detail_info=Syarat dan Ketentuan :\n\n- Cashback Rp 50 ribu untuk transaksi minimal Rp 500 ribu/struk belanja dengan Kartu Kredit dan Debit BNI di Matahari Department Store.\n- Cashback akan diberikan per customer name untuk Kartu Kredit BNI selama periode program\n- Cashback Rp 50 ribu akan dikreditkan minimal 1 (satu) bulan setelah periode tanggal transaksi melalui sistem BNI.\n- Program berlaku di seluruh outlet Matahari Dept Store di Indonesia.\n- Promo berlaku untuk semua jenis Kartu Kredit dan Debit BNI kecuali Kartu Kredit Garuda Platinum dan Signature, iB Hasanah, Corporate Card dan Kartu Debit Syariah.\n- Syarat dan ketentuan lainnya berlaku."
        #         }
        #     ]
        # },
        # {
        #     "title": "BERRYBENKA",
        #     "subtitle": "Diskon 30% di BERRYBENKA.com dengan Kartu Kredit BNI",
        #     "image_url": "https://m.bnizona.com//files/2e0fc6f02fc6326f18d02afcef1c107d.jpg",
        #     "buttons": [
        #         {
        #             "type": "postback",
        #             "title": "Detail Info",
        #             "payload": "&evt=info_promo&detail_info=Syarat dan Ketentuan :\n\n- Diskon 30% maksimal Rp 150 ribu di www.berrybenka.com/bni\n- Promo hanya berlaku di hari Rabu dan Sabtu.\n- Discount berlaku untuk semua produk.\n- Tidak ada minimum pembelanjaan.\n- Discount tidak dapat digabungkan dengan dengan promo lain.\n- Promo berlaku untuk semua Kartu Kredit BNI (kecuali iB Hasanah dan Corporate Card)\n- Periode promo : hingga 05 Agustus 2017"
        #         }
        #     ]
        # }
                                   ]
    data_template_promo_makanan = [
    {
                "title": "Pringsewu Resto",
                "subtitle" : "Diskon 20% di Pringsewu Group",
                "image_url": "https://bangjoni.com/images/bni/Carousel-Menu_Food-Promo02.jpg",
                "buttons": [
                    {
                        "type":"postback",
                        "title":"Detail Info",
                        "payload":"&evt=info_promo&detail_info=-Diskon 20% berlaku untuk transaksi pembelian food dan beverage (khusus menu ala carte).\n- Minimal transaksi Rp 200.000 berlaku di Resto Pringsewu.\n- Minimal transaksi Rp 100.000 berlaku di Mie Pasar Baru dan RM Kabayan.\n- Tidak berlaku kelipatan dan split transaksi dan hanya berlaku untuk dine in dan delivery.\n- Promo berlaku untuk semua jenis Kartu Kredit BNI kecuali Corporate Card dan Hasanah Card.\n- Berlaku di semua resto Pringsewu Group."
                    }
                ]
            },
        {
                "title": "CFC",
                "subtitle" : "Free Ayam setiap Senin dan Free Upsize di hari lain dengan Kartu Debit BNI di CFC",
                "image_url": "https://bangjoni.com/images/bni/Carousel-Menu_Food-Promo01.jpg",
                "buttons": [
                    {
                        "type":"postback",
                        "title":"Detail Info",
                        "payload":"&evt=info_promo&detail_info=Syarat dan Ketentuan:\n\n- Free Ayam setiap Senin untuk transaksi minimal Rp 50 ribu.\n- Maksimum free ayam 2 pcs.\n- Free upsize untuk pembelian Paket  Astaga setiap Selasa - Minggu.\n- maksimum 4 paket yang akan mendapatkan free upsize.\n- Berlaku untuk Kartu Debit BNI berlogo MasterCard kecuali BNI Debit Syariah.\n- Berlaku hingga 30 November 2017."
                    }
                ]
            },
    {
                "title": "BAKMI GM",
                "subtitle" : "Gratis Pangsit Goreng 5 Pcs di Bakmi GM",
                "image_url": "https://bangjoni.com/images/bni/Carousel-Menu_Food-Promo03.jpg",
                "buttons": [
                    {
                        "type":"postback",
                        "title":"Detail Info",
                        "payload":"&evt=info_promo&detail_info=-Gratis Pangsit Goreng isi 5 dengan minimum transaksi  Rp 125.000,- (sebelum pajak).\n- Berlaku untuk semua Kartu Debit BNI berlogo MasterCard, kecuali Kartu Debit BNI Syariah.\n- Berlaku di seluruh outlet Bakmi GM di seluruh Indonesia, kecuali Store Bandara dan Stasiun.\n- Berlaku untuk santap di tempat (dine in).\n- Promo berlaku hingga 31 Agustus 2017"
                    }
                ]
            }
    # {
    #             "title": "Cavinton Hotel Yogyakarta",
    #             "subtitle" : "Diskon 30% Room dan 10% Food di Cavinton Hotel",
    #             "image_url": "https://m.bnizona.com//files/31db8bc2031fec52d2da3ebee60c92ff.JPG",
    #             "buttons": [
    #                 {
    #                     "type":"postback",
    #                     "title":"Detail Info",
    #                     "payload":"&evt=info_promo&detail_info=Syarat dan Ketentuan:\n\n- Diskon 30% berlaku untuk Room dengan Kartu Kredit dan Debit BNI.\n- Diskon 10% berlaku untuk Food Only dengan Kartu Kredit dan Debit BNI.\n- Berlaku bagi pengguna Kartu Kredit dan Debit BNI kecuali iB  Hasanah, Corporate Card dan Debit Syariah.\n- Berlaku hingga 10 November 2017."
    #                 }
    #             ]
    #         },
    # {
    #             "title": "Grand Aston Hotel Yogyakarta",
    #             "subtitle" : "Special Rate Room dan Diskon 15% Food and Beverage di Grand Aston Hotel Yogyakarta",
    #             "image_url": "https://m.bnizona.com//files/31003ab28aee0b0f94af936cb8a78ccf.JPG",
    #             "buttons": [
    #                 {
    #                     "type":"postback",
    #                     "title":"Detail Info",
    #                     "payload":"&evt=info_promo&detail_info=Syarat dan Ketentuan:\n\n- Special Rate untuk Room dari Publish Rate dengan Kartu Kredit BNI (tidak termasuk atau tidak bisa digunakan untuk harga promosi, holiday season, long weekend, lebaran, natal dan tahun baru).\n- Diskon 15% untuk food dan beverage dengan Kartu Kredit BNI (tidak berlaku untuk minuman beralkohol).\n- Berlaku bagi pengguna Kartu Kredit BNI kecuali iB Hasanah dan Corporate Card\n- Berlaku hingga 31 Desember 2017"
    #                 }
    #             ]
    #         },
    # {
    #             "title": "Eastparc Hotel Yogyakarta",
    #             "subtitle" : "Diskon hingga 50% di Eastparc Hotel Yogyakarta",
    #             "image_url": "https://m.bnizona.com//files/eb760f82d784ac7899bd790109e8a356.JPG",
    #             "buttons": [
    #                 {
    #                     "type":"postback",
    #                     "title":"Detail Info",
    #                     "payload":"&evt=info_promo&detail_info=Syarat dan Ketentuan:\n\n- Diskon 50% untuk room dari Publish rate dengan Kartu Kredit dan Debit BNI.\n- Diskon 15% untuk Konsumsi di Verandah Restaurant dan Verandah Alfresco dengan Kartu Kredit dan Debit BNI.\n- Diskon tidak berlaku untuk periode Idul Fitri, Natal dan Tahun Baru.\n- Berlaku bagi pengguna Kartu Kredit dan Debit BNI kecuali iB Hasanah, Corporate Card dan Debit BNI Syariah.\n- Berlaku hingga 15 Februari 2018."
    #                 }
    #             ]
    #         },
    # {
    #             "title": "Grand Quality Hotel",
    #             "subtitle" : "Diskon hingga 25% di Grand Quality Hotel Yogyakarta",
    #             "image_url": "https://m.bnizona.com//files/3a50d45d8af8d4b028fed25fb8589c80.JPG",
    #             "buttons": [
    #                 {
    #                     "type":"postback",
    #                     "title":"Detail Info",
    #                     "payload":"&evt=info_promo&detail_info=Syarat dan Ketentuan:\n\n- Diskon 25% berlaku untuk Room dengan Kartu Kredit dan Debit BNI (tidak termasuk atau tidak bisa digunakan untuk harga promosi, holiday season, long weekend, lebaran, natal dan tahun baru).\n- Diskon 20% berlaku untuk Food Only di Coffe Shop, Nagoya Japanese Restaurant dan Serayu Seafood Restaurant dengan Kartu Kredit dan Debit BNI (berlaku hanya untuk menu Ala Carte).\n- Diskon 10 % untuk Spa Package di Warm Spa & Fitness Center.\n- Berlaku bagi pengguna Kartu Kredit dan Debit BNI kecuali iB Hasanah, Corporate Card dan Debit BNI Syariah.\n- Berlaku hingga 31 Januari 2018."
    #                 }
    #             ]
    #         },
    # {
    #             "title": "Grand Quality Hotel",
    #             "subtitle" : "Diskon hingga 25% di Grand Quality Hotel Yogyakarta",
    #             "image_url": "https://m.bnizona.com//files/3a50d45d8af8d4b028fed25fb8589c80.JPG",
    #             "buttons": [
    #                 {
    #                     "type":"postback",
    #                     "title":"Detail Info",
    #                     "payload":"&evt=info_promo&detail_info=Syarat dan Ketentuan:\n\n- Diskon 25% berlaku untuk Room dengan Kartu Kredit dan Debit BNI (tidak termasuk atau tidak bisa digunakan untuk harga promosi, holiday season, long weekend, lebaran, natal dan tahun baru).\n- Diskon 20% berlaku untuk Food Only di Coffe Shop, Nagoya Japanese Restaurant dan Serayu Seafood Restaurant dengan Kartu Kredit dan Debit BNI (berlaku hanya untuk menu Ala Carte).\n- Diskon 10 % untuk Spa Package di Warm Spa & Fitness Center.\n- Berlaku bagi pengguna Kartu Kredit dan Debit BNI kecuali iB Hasanah, Corporate Card dan Debit BNI Syariah.\n- Berlaku hingga 31 Januari 2018."
    #                 }
    #             ]
    #         }
    ]

    data_template_promo_gadget = [
    {
                "title": "ERAFONE",
                "subtitle" : "Cashback hingga Rp 500 ribu + Cicilan 0% di PRJ 2017 dengan Kartu Kredit BNI",
                "image_url": "https://bangjoni.com/images/bni/Carousel-Menu_Gadget-Promo01.jpg",
                "buttons": [
                    {
                        "type":"postback",
                        "title":"Detail Info",
                        "payload":"&evt=info_promo&detail_info=Mekanisme :\n- Cashback Rp 200 ribu setiap transaksi minimal Rp 3.000.000,- untuk 60 orang pertama dengan menggunakan Kartu Kredit BNI.\n- Cashback Rp 300 ribu setiap transaksi minimal Rp 5.000.000,- untuk 50 orang pertama dengan menggunakan Kartu Kredit BNI.\n- Cashback Rp 500 ribu setiap transaksi minimal Rp 10.000.000,- untuk 40 orang pertama dengan menggunakan Kartu Kredit BNI.\n- Cashback digabungkan program BNI Installment 0 persen tenor sd 24 bulan langsung di EDC BNI."
                    }
                ]
            },
    {
                "title": "ERAFONE",
                "subtitle" : "Diskon 100 Ribu di Erafone.com dengan Kartu Kredit BNI",
                "image_url": "https://bangjoni.com/images/bni/Carousel-Menu_Gadget-Promo02.jpg",
                "buttons": [
                    {
                        "type":"postback",
                        "title":"Detail Info",
                        "payload":"&evt=info_promo&detail_info=Syarat dan Ketentuan:\n- Diskon Rp 100 ribu untuk 15 transaksi pertama di setiap hari Senin dengan minimum transaksi Rp 1,5 juta dengan menggunakan Kartu Kredit BNI.\n- Diskon langsung memotong harga produk.\n- Berlaku setiap hari Senin hingga tanggal 25 Desember 2017.\n- Berlaku untuk semua jenis Kartu Kredit BNI kecuali Corporate Card, BNI-JCB dan iB Hasanah Card.\n- Pembelian dilakukan di Erafone.com\n- Diskon wajib digabungkan dengan cicilan 0% hingga 12 bulan langsung di IPG BNI.\n- Pembelian dibatasi maksimal 1 kuota diskon untuk 1 pemegang kartu setiap hari Senin."
                    }
                ]
            },
        {
            "title": "Swiss-Belhotel International",
            "subtitle": "Beli Samsung dapat Samsung di Best N Cheap - Pekanbaru",
            "image_url": "https://bangjoni.com/images/bni/Carousel-Menu_Gadget-Promo03.jpg",
            "buttons": [
                {
                    "type": "postback",
                    "title": "Detail Info",
                    "payload": "&evt=info_promo&detail_info=1. Menangkan hadiah langsung dengan minimal transaksi Rp 2,5 juta khusus pengguna Kartu Kredit BNI :\n- Galaxy A7 2017 1 (satu) unit\n- Galaxy A5 2017 1 (satu) unit\n- Samsung J2 Prime 3 (tiga) unit\n- Samsung Lipat 1272 12 (dua belas) unit\n- dan hadiah menarik lainnya\n\n2. Hemat hingga 50% dengan Redeem Point atau maksimal redeem Rp.1.000.000,-  (1 point = Rp.5,-)\n\n3. Berlaku cicilan 0% tenor 6&12 bulan\n\n4. Berlaku untuk seluruh jenis Kartu Kredit BNI kecuali iB Hasanah card dan Corporate card\n\n5. Berlaku setiap hari selama periode program termasuk hari libur Nasional dan Lokal\n\n6. Syarat dan Ketentuan berlaku."
                }
            ]
        }
    ]