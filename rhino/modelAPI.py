from concurrent import futures




def fetcher(urls):
    def fetcher_one(url):
        try:
            return url, requests.get(url, timeout=10).status_code
        except:
            return url, 666
    with futures.ThreadPoolExecutor(max_workers=2) as executor:
        for rst in executor.map(fetcher_one, urls):
            yield rst


if __name__ == '__main__':
    fetcher(['http://www.baidu.com', 'http://soso.com'])