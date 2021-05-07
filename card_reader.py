import binascii
import nfc

class CardReader(object):
    def on_connect(self, tag):
        print("読み取り中")
        self.idm = binascii.hexlify(tag.idm)
        return True
    def read_idm(self):
        self.idm = ""
        clf = nfc.ContactlessFrontend('usb')
        try:
            print("カードをタッチしてください")
            clf.connect(rdwr = {'on-connect': self.on_connect})
        finally:
            clf.close()