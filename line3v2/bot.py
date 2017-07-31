from data import template_carousel ,template_confirm, template_img_buttons
from linebot import LineBotApi
from linebot.models import ImageSendMessage
from linebot.models import LocationSendMessage
from linebot.models import StickerSendMessage
from linebot.models import TextSendMessage
from linebot.models import VideoSendMessage

from line3v2.data import template_imagemap


class Bot(object):
    """
    Implementation of https://github.com/line/line-bot-sdk-python
    """

    def __init__(self, token):
        self.line_bot_api = LineBotApi(token)

    def __send_multicast(self, user_ids, payload):
        """
        Send message payload to one or more user ID

        :param user_ids:
        :param payload:
        :return:
        """
        # print payload
        self.line_bot_api.multicast(user_ids, payload)

    # def __refreshToken(self):

    def get_profile(self, user_id):
        """
        Get profile detail from user_id

        :param user_id:
        :return profile:
        """
        profile = self.line_bot_api.get_profile(user_id)
        return profile

    def send_text_message(self, user_ids, text):
        """
        Send basic text message to specific user ID.
        If you want to send to more than one user ID, use comma to separate them.
        Message text basically will split if delimiter found

        :param user_ids:
        :param text:
        :return:
        """

        payloads = []
        user_ids = user_ids.split(",")
        messages = text.split("<br>")
        for msg in messages:
            if not msg :
                continue
            payloads.append(TextSendMessage(text=msg.strip()))
        # print payloads

        if len(payloads) > 0:
            looper = 5
            start_idx = 0
            end_idx = 5
            remaining_payloads = len(payloads)
            while remaining_payloads > 0:
                self.__send_multicast(user_ids, payloads[start_idx:end_idx])
                start_idx = start_idx + looper
                end_idx = end_idx + looper
                remaining_payloads = remaining_payloads - looper

    def send_image_message(self, user_ids, img_url, **params):
        """
        Send basic image message specific one or more user ID.
        More detail about specifications : https://devdocs.line.me/en/#send-message-object Image section

        :param user_ids:
        :param img_url:
        :param params:
        :return:
        """
        user_ids = user_ids.split(",")
        # if params is not None :
        #     thumbnail = params.get("thumbnail") if params.has_key("thumbnail") else None
        #     self.__send_multicast(user_ids, ImageSendMessage(
        #             original_content_url=img_url,
        #             preview_image_url=thumbnail if thumbnail is not None else img_url
        #         ))
        # else :
        self.__send_multicast(user_ids, ImageSendMessage(
            original_content_url=img_url,
            preview_image_url=img_url
        ))

    def send_video_message(self, user_ids, video_url, thumbnail_img_url):
        """
        Send video message specific one or more user ID.
        More detail about specifications : https://devdocs.line.me/en/#send-message-object Video section

        :param user_ids:
        :param video_url:
        :param thumbnail_img_url:
        :return:
        """
        user_ids = user_ids.split(",")
        self.__send_multicast(user_ids, VideoSendMessage(
                original_content_url=video_url,
                preview_image_url=thumbnail_img_url
            ))

    def send_sticker_message(self, user_ids, sticker_id, package_id):
        """
        Send fancy sticker message specific one or more user ID.
        More detail about specifications : https://devdocs.line.me/en/#send-message-object Sticker section

        :param user_ids:
        :param sticker_id:
        :param package_id:
        :return:
        """
        user_ids = user_ids.split(",")
        self.__send_multicast(user_ids, StickerSendMessage(
                package_id=package_id,
                sticker_id=sticker_id
            ))

    def send_location_message(self, user_ids, title, address, latitude, longitude):
        """
        Send location message specific one or more user ID.
        More detail about specifications : https://devdocs.line.me/en/#send-message-object Location section

        :param user_ids:
        :param title:
        :param address:
        :param latitude:
        :param longitude:
        :return:
        """
        user_ids = user_ids.split(",")
        self.__send_multicast(user_ids, LocationSendMessage(
                title=title,
                address=address,
                latitude=latitude,
                longitude=longitude
            ))

    def send_imagemap(self, user_ids, imagemap_id):
        """
        Send imagemap to message specific one or more user ID.
        Pass a valid imagemap_id from template_imagemap.py, otherwise invalid imagemap id exception will be raised

        :param user_ids:
        :param imagemap_id:
        :return:
        """
        for payload_object in template_imagemap.imagemaps:
            if payload_object["id"] == imagemap_id:
                payload = payload_object["payload"]
                found = True

        if found is True:
            user_ids = user_ids.split(",")
            self.__send_multicast(user_ids, payload)
        else :
            raise Exception('Invalid imagemap ID!')

    def send_image_button(self, user_ids, img_button_id):
        """
        Send image button message to specific one or more user ID.
        Pass a valid image button id from template_img_buttons.py, otherwise invalid id exception will be raised

        :param user_ids:
        :param img_button_id:
        :return:
        """
        for payload_object in template_img_buttons.imgbuttons:
            if payload_object["id"] == img_button_id:
                payload = payload_object["payload"]
                found = True

        if found is True:
            user_ids = user_ids.split(",")
            self.__send_multicast(user_ids, payload)
        else:
            raise Exception('Invalid image button ID!')

    def send_link_message(self, user_ids, alt_text, thumbnail_url, title, description, label, uri):
        payload = template_img_buttons.compose_img_buttons(alt_text, thumbnail_url, title, description, [{'type' : 'uri', 'label' : label, 'uri' : uri}])
        user_ids = user_ids.split(",")
        self.__send_multicast(user_ids, payload)

    def send_confirmation(self, user_ids, confirm_id):
        """
        Send confirmation message to specific one or more user ID.
        Pass a valid confirmation_id from template_confirmation.py, otherwise invalid confirmation id exception will be raised

        :param user_ids:
        :param confirm_id:
        :return:
        """
        for payload_object in template_confirm.confirmations:
            if payload_object["id"] == confirm_id:
                payload = payload_object["payload"]
                found = True

        if found is True:
            user_ids = user_ids.split(",")
            self.__send_multicast(user_ids, payload)
        else:
            raise Exception('Invalid imagemap ID!')

    def send_carousel(self, user_ids, carousel_id):
        """
        Send carousel message to specific one or more user ID.
        Pass a valid carousel_id from template_carousel.py, otherwise invalid carousel id exception will be raised

        :param user_ids:
        :param carousel_id:
        :return:
        """
        for payload_object in template_carousel.carousels:
            if payload_object["id"] == carousel_id:
                payload = payload_object["payload"]
                found = True

        if found is True:
            user_ids = user_ids.split(",")
            self.__send_multicast(user_ids, payload)
        else:
            raise Exception('Invalid imagemap ID!')

    def send_composed_carousel(self, user_ids, alt_text, columns):
        payload = template_carousel.composeCarousel(alt_text, columns)
        user_ids = user_ids.split(",")
        self.__send_multicast(user_ids, payload)

    def send_composed_confirm(self, user_ids, alt_text, text, option1, option2):
        payload = template_confirm.composeConfirm(alt_text, text, option1, option2)
        user_ids = user_ids.split(",")
        self.__send_multicast(user_ids, payload)

    def send_composed_img_buttons(self, user_ids, alt_text, thumbnail_url, title, description, actions):
        payload = template_img_buttons.compose_img_buttons(alt_text, thumbnail_url, title, description, actions)
        user_ids = user_ids.split(",")
        self.__send_multicast(user_ids, payload)

