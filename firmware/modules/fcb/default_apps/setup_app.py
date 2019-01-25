import json


class App:
    _STATE_GETTING_NAME = 1
    _STATE_GETTING_SOCIAL = 2
    _STATE_GETTING_TICKET_ID = 3
    _STATE_DONE = 4

    def __init__(self, fcb):
        self._fcb = fcb
        self._state = self._STATE_GETTING_NAME
        self._data = {
            "name": None,
            "social_handle": None,
            "ticket_id": None
        }

    def handle_event(self, evt):
        pass

    def redraw(self):
        if self._state == self._STATE_GETTING_NAME:
            name = self._fcb.get_input("Name: ")
            self._state = self._STATE_GETTING_SOCIAL
            self._data["name"] = name

        elif self._state == self._STATE_GETTING_SOCIAL:
            social = self._fcb.get_input("Social handle: ")
            self._state = self._STATE_GETTING_TICKET_ID
            self._data["social_handle"] = social

        elif self._state == self._STATE_GETTING_TICKET_ID:
            ticket_id = self._fcb.get_input("Ticket ID: ")
            self._state = self._STATE_DONE
            self._data["ticket_id"] = ticket_id

        elif self._state == self._STATE_DONE:
            conf_f = open("/config.json", "w")
            json.dump(self._data, conf_f)
            conf_f.close()
            self._fcb.app_exit()
