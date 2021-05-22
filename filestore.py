class FileStore:
    def __init__(self ,word):
        pass

    def download_as_csv(self):
        print("OK")

    def download_into_mongo_db(self):
        print("Nice")

if __name__ == '__main__':
    fileStore = FileStore("helloworld")
    fileStore.download_as_csv()