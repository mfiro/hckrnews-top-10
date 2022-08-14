from top10.hn import Client

if __name__ == '__main__':
    hn_client = Client()

    # get best stories
    best = hn_client.get_beststories()

    item = hn_client.get_item(best[-1])

    print(item)