import binascii
import nfc
import os
import sys
import requests
import json

grbGroupId=None


class CardReader():
    def on_connect(self, tag):
        #タッチ時の処理
        print("[INFO]Card Touch")

        if self.idm == "00000000000000":
            print("カードが正しく読み取れませんでした")
        else:
            print("---Show info---")


            #タグ情報を全て表示
            print(tag)

            #IDmのみ取得して表示
            self.idm = binascii.hexlify(tag._nfcid)
            print("IDm:" + str(self.idm))

            #出席の情報についてのPOSTリクエストを送信
            response=requests.post("https://felica-attendance-manager.azurewebsites.net/api/rooms/"+grbGroupId+"/update?idm="+self.idm)
            print("Status:"+response.text);

            #名前の情報についてのGETリクエストを送信
            name=requests.get("https://felica-attendance-manager.azurewebsites.net/api/name/get?idm="+self.idm);
            if name.text=="":
                print("Name:"+self.idm);
            else:
                print("Name:"+name.text);

            return True

        def read_id(self):
            clf = nfc.ContactlessFrontend('usb')
            try:
                clf.connect(rdwr={'on-connect': self.on_connect})
            finally:
                clf.close()

if __name__ == '__main__':
    #グループIDが指定されているかの確認
    try:
        groupId=sys.argv[1]
    except IndexError:
        print("グループIDが指定されていません")
        sys.exit(-1)

    #グループIDの一覧を取得する
    response=requests.get("https://felica-attendance-manager.azurewebsites.net/api/rooms/show")
    my_list = json.loads(response.text)

    if (groupId in my_list):
        grbGroupId=groupId
    else:
        print("指定したGroup IDは数字ではありません")

    cr = CardReader()
    while True:
        #最初に表示
        print("カードリーダーにタッチしてください")

        #タッチ待ち
        cr.read_id()

        #リリース時の処理
        print("---Released---")
