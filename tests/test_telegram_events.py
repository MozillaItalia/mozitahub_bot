import unittest

from telegram_events import events


class TelegramEventsTestCase(unittest.TestCase):

    def build_expected(self, text, type_msg, modificato, risposta):
        return {
            "text": text,
            "type_msg": type_msg,
            "modificato": modificato,
            "risposta": risposta,
        }

    def test_events_handles_data_correctly(self):
        fixtures = [
            (
                ({"text": "", "edit_date": ""}, ["NM"], ""),
                self.build_expected("", "NM", True, False)
            ),
            (
                ({"text": "", "reply_to_message": ""}, ["NM"], ""),
                self.build_expected("", "NM", False, True)
            ),
            (
                ({"text": "",}, [], ["response"]),
                self.build_expected("|| Messaggio non identificato o non consentito ||\n >> >> Response: ['response']", "NI", False, False)
            ),
            (
                ({"text": "", "entities": [{"type": ""}]}, ["NM"], ""),
                self.build_expected("", "NM", False, False)
            ),
            (
                ({"text": "", "entities": [{"type": "mention"}]}, ["T"], ""),
                self.build_expected("", "T", False, False)
            ),
            (
                ({"text": "", "entities": [{"type": "url"}]}, ["LK"], ""),
                self.build_expected("", "LK", False, False)
            ),
            (
                ({"text": "", "entities": [{"type": "bot_command"}]}, ["LK"], ""),
                self.build_expected("", "LK", False, False)
            ),
            (
                ({"data": ["data"]}, [], ""),
                self.build_expected("['data']", "BIC", False, False)
            ),
            (
                ({"new_chat_participant": {"id": 0}, "from": {"id": 1}}, [], ""),
                self.build_expected("|| Un utente è stato aggiunto ||", "JA", False, False)
            ),
            (
                ({"new_chat_participant": {"id": 1}, "from": {"id": 1}}, [], ""),
                self.build_expected("|| Un utente è entrato ||", "J", False, False)
            ),
            (
                ({"left_chat_participant": {"id": 0}, "from": {"id": 1}}, [], ""),
                self.build_expected("|| Un utente è stato rimosso ||", "LR", False, False)
            ),
            (
                ({"left_chat_participant": {"id": 1}, "from": {"id": 1}}, [], ""),
                self.build_expected("|| Un utente è uscito ||", "L", False, False)
            ),
            (
                ({"document": "", "caption": ["caption"]}, ["D"], ""),
                self.build_expected("|| Documento ||\n >> >> Didascalia documento: ['caption']", "D", False, False)
            ),
            (
                ({"document": "",}, ["D"], ""),
                self.build_expected("|| Documento ||", "D", False, False)
            ),
            (
                ({"voice": "",}, ["VM"], ""),
                self.build_expected("|| Messaggio vocale ||", "VM", False, False)
            ),
            (
                ({"video_note": "",}, ["VMSG"], ""),
                self.build_expected("|| Video messaggio ||", "VMSG", False, False)
            ),
            (
                ({"photo": "", "caption": ["caption"]}, ["I"], ""),
                self.build_expected("|| Immagine/Foto ||\n >> >> Didascalia immagine/foto: ['caption']", "I", False, False)
            ),
            (
                ({"photo": "",}, ["I"], ""),
                self.build_expected("|| Immagine/Foto ||", "I", False, False)
            ),
            (
                ({"music": "", "caption": ["caption"]}, ["M"], ""),
                self.build_expected("|| Musica/Audio ||\n >> >> Didascalia musica/audio: ['caption']", "M", False, False)
            ),
            (
                ({"music": "",}, ["M"], ""),
                self.build_expected("|| Musica/Audio ||", "M", False, False)
            ),
            (
                ({"video": "", "caption": ["caption"]}, ["V"], ""),
                self.build_expected("|| Video ||\n >> >> Didascalia video: ['caption']", "V", False, False)
            ),
            (
                ({"video": "",}, ["V"], ""),
                self.build_expected("|| Video ||", "V", False, False)
            ),
            (
                ({"contact": "", "caption": ["caption"]}, ["C"], ""),
                self.build_expected("|| Contatto ||\n >> >> Didascalia contatto: ['caption']", "C", False, False)
            ),
            (
                ({"contact": "",}, ["C"], ""),
                self.build_expected("|| Contatto ||", "C", False, False)
            ),
            (
                ({"location": "",}, ["P"], ""),
                self.build_expected("|| Posizione ||", "P", False, False)
            ),
            (
                ({"sticker": {"emoji": "emoji"},}, ["S"], ""),
                self.build_expected("(sticker) emoji", "S", False, False)
            ),
            (
                ({"animation": "",}, ["G"], ""),
                self.build_expected("|| Immagine GIF ||", "G", False, False)
            ),
            (
                ({"new_chat_photo": "",}, [], ""),
                self.build_expected("|| Immagine chat aggiornata ||", "NCP", False, False)
            ),
            (
                ({}, [], ["response"]),
                self.build_expected("|| Messaggio non identificato o non consentito ||\n >> >> Response: ['response']", "NI", False, False)
            ),
        ]
        for i, (params, expected) in enumerate(fixtures):
            with self.subTest(i=i, params=params):
                self.assertEqual(events(*params), expected)
