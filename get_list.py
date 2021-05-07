from card_reader import CardReader
from database_manager import DatabaseManager

if __name__ == '__main__':
    cr = CardReader()
    print() 
    cr.read_idm()
    new_idm = str(cr.idm)
    new_idm = new_idm[2:-1]
    print("カードのID: ",end=' ')
    print(new_idm)

    while True:
        text = input('登録名を入力してください >> ')
        print()
        is_inp = input(text + "さんでよろしいですか？ 'y/n' >> ")
        if is_inp is ('n' or 'no'  or 'N'):
            print("N")
            break
        elif is_inp is not ('y' or 'yes' or 'Y'):
            print("y/n で入力してください")
            continue
        else:
            print("Y")
            with DatabaseManager() as dm:
                dm.subscribe(new_idm, text)
            break
