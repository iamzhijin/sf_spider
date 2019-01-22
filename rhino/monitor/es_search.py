from rhino.settings import ELASTIC_SEARCH_SERVER
from rhino.settings import ELASTIC_SEARCH_PORT
from elasticsearch import Elasticsearch
from datetime import date
from datetime import timedelta
import re


class EsMan:
    def __init__(self):
        self.es_server = ELASTIC_SEARCH_SERVER
        self.es_port = ELASTIC_SEARCH_PORT
        es_address = self.es_server + ":" + self.es_port
        self.es = Elasticsearch([es_address], timeout=60)

    def total(self, url):
        index, doc_type = self.split_url(url)
        query = {"_source": ""}
        rst = self.es.search(index=index, doc_type=doc_type, body=query)
        return rst['hits']['total']

    def agg_day_source(self, url, begin=None, end=None):

        index, doc_type = self.split_url(url)
        agg_time_field = 'update_time' if \
            index == 'judge_doc' or \
            index == 'executive_announcement' or \
            index == 'shixin_beizhixing' or \
            index == 'exposure_desk' else 'create_time'
        if not begin and not end:
            begin = date(year=2016, month=1, day=1)
            end = date.today()

        query = {
            "size": 0,
            "query": {
                "bool": {
                    "must": [{
                        "range": {
                            agg_time_field: {
                                "gte": begin.isoformat(),
                                "lte": end.isoformat(),
                                "format": "yyyy-MM-dd"
                            }
                        }
                    }]
                }
            },
            "aggs": {
                "create_time_agg": {
                    "date_histogram": {
                        "field": agg_time_field,
                        "interval": "day"
                    }
                }
            }
        }

        rst = self.es.search(index=index, doc_type=doc_type, body=query)
        result, _time = [], []
        for item in rst['aggregations']['create_time_agg']['buckets']:
            crawl_time = item['key_as_string']
            crawl_time = re.findall('(\d+)-(\d+)-(\d+)T', crawl_time)[0]
            crawl_time = date(
                year=int(crawl_time[0]),
                month=int(crawl_time[1]),
                day=int(crawl_time[2]))
            result.append({
                "crawl_time": crawl_time.isoformat(),
                "count": item['doc_count']
            })
            _time.append(crawl_time.isoformat())
        for d in range(1, int((end - begin).days) + 1):
            _d = (begin + timedelta(d)).isoformat()
            if _d not in _time:
                _time.append(_d)
                result.append({"crawl_time": _d, "count": 0})
        return sorted(result, key=lambda a: a['crawl_time'])

    @staticmethod
    def split_url(url):
        index, doc_type = url.split('/', 2)
        return index, doc_type

    def source_sort_by_time(self, url):
        # 每个源通过时间排序的第一条结果
        index, doc_type = self.split_url(url)
        sources = {''}
        agg_time_field = 'update_time' if \
            index == 'judge_doc' or \
            index == 'executive_announcement' or \
            index == 'shixin_beizhixing' or \
            index == 'exposure_desk' else 'create_time'
        try:
            query = {
                "_source": "{}",
                "aggs": {
                    "source_last_update": {
                        "terms": {
                            "field": "source",
                            "size": 1000
                        },
                        "aggs": {
                            "create_time_agg": {
                                "terms": {
                                    "field": agg_time_field,
                                    "size": 1,
                                    "order": {
                                        "_term": "desc"
                                    }
                                }
                            }
                        }
                    }
                }
            }

            rst = self.es.search(index=index, doc_type=doc_type, body=query)
        except:
            query = {
                "_source": "{}",
                "aggs": {
                    "source_last_update": {
                        "terms": {
                            "field": "source.keyword",
                            "size": 1000
                        },
                        "aggs": {
                            "create_time_agg": {
                                "terms": {
                                    "field": agg_time_field,
                                    "size": 1,
                                    "order": {
                                        "_term": "desc"
                                    }
                                }
                            }
                        }
                    }
                }
            }

            rst = self.es.search(index=index, doc_type=doc_type, body=query)

        for bucket in rst['aggregations']['source_last_update']['buckets']:
            if bucket['create_time_agg']['buckets']:
                crawl_time = bucket['create_time_agg']['buckets'][0][
                    'key_as_string']
                crawl_time = re.findall('(\d+)-(\d+)-(\d+)T', crawl_time)[0]
                crawl_time = date(
                    year=int(crawl_time[0]),
                    month=int(crawl_time[1]),
                    day=int(crawl_time[2]))
                yield {'source': bucket['key'], 'crawl_time': crawl_time}

    # 当天fail_recode统计
    def agg_fail_record(self, source):
        url = 'fail_record/fail_record'
        index, doc_type = self.split_url(url)
        # .isoformat()
        today = date.today()
        yesterday = (today - timedelta(days=1))

        query = {
            "size": 0,
            "query": {
                "bool": {
                    "must": [{
                        "range": {
                            "create_time": {
                                "gte": yesterday.isoformat(),
                                "lte": today.isoformat(),
                                "format": "yyyy-MM-dd"
                            }
                        }
                    }, {
                        "term": {
                            "data.source": {
                                "value": source
                            }
                        }
                    }]
                }
            }
        }
        rst = self.es.search(index=index, doc_type=doc_type, body=query)

        return rst['hits']['total']

    def mapping(self, url, source):
        index, doc_type = self.split_url(url)
        rst = self.es.indices.get_mapping(index, doc_type)

        for item in rst[index]['mappings'][doc_type]['properties']:

            query = {
                "_source": "",
                "query": {
                    "bool": {
                        "must": [{
                            "exists": {
                                "field": item
                            }
                        }, {
                            "term": {
                                "source": {
                                    "value": source
                                }
                            }
                        }]
                    }
                }
            }
            rst = self.es.search(index=index, doc_type=doc_type, body=query)

            query_total = {
                "_source": "",
                "query": {
                    "bool": {
                        "must": [{
                            "term": {
                                "source": {
                                    "value": source
                                }
                            }
                        }]
                    }
                }
            }
            rst_total = self.es.search(
                index=index, doc_type=doc_type, body=query_total)

            yield {
                'field': item,
                'count': rst['hits']['total'],
                'total': rst_total['hits']['total']
            }

    def crawled_uncrawled_project(self, url):
        index, doc_type = self.split_url(url)
        agg_time_field = 'update_time' if \
            index == 'judge_doc' or \
            index == 'executive_announcement' or \
            index == 'shixin_beizhixing' or \
            index == 'exposure_desk' else 'create_time'
        today = date.today()
        try:
            query = {
                "_source": "",
                "size": 0,
                "query": {
                    "bool": {
                        "must": [{
                            "range": {
                                agg_time_field: {
                                    "gte": today.isoformat(),
                                    "lte": today.isoformat(),
                                    "format": "yyyy-MM-dd"
                                }
                            }
                        }]
                    }
                },
                "aggs": {
                    "source": {
                        "terms": {
                            "field": "source",
                            "size": 100000
                        }
                    }
                }
            }

            rst = self.es.search(index=index, doc_type=doc_type, body=query)
        except:
            query = {
                "_source": "",
                "size": 0,
                "query": {
                    "bool": {
                        "must": [{
                            "range": {
                                agg_time_field: {
                                    "gte": today.isoformat(),
                                    "lte": today.isoformat(),
                                    "format": "yyyy-MM-dd"
                                }
                            }
                        }]
                    }
                },
                "aggs": {
                    "source": {
                        "terms": {
                            "field": "source.keyword",
                            "size": 100000
                        }
                    }
                }
            }
            rst = self.es.search(index=index, doc_type=doc_type, body=query)
        try:
            query = {
                "_source": "{}",
                "size": 0,
                "aggs": {
                    "source": {
                        "terms": {
                            "field": "source",
                            "size": 100000
                        }
                    }
                }
            }
            un_rst = self.es.search(index=index, doc_type=doc_type, body=query)
        except:
            query = {
                "_source": "{}",
                "size": 0,
                "aggs": {
                    "source": {
                        "terms": {
                            "field": "source.keyword",
                            "size": 100000
                        }
                    }
                }
            }
            un_rst = self.es.search(index=index, doc_type=doc_type, body=query)
        return [{
            "value": len(rst['aggregations']['source']['buckets']),
            "name": '有更新爬虫'
        }, {
            "value":
            len(un_rst['aggregations']['source']['buckets']) -
            len(rst['aggregations']['source']['buckets']),
            "name":
            "无更新爬虫"
        }]

    def project_all_total(self, url):
        index, doc_type = self.split_url(url)
        query = {"_source": "{}", "size": 0}
        rst = self.es.search(index=index, doc_type=doc_type, body=query)
        return rst['hits']['total']

    def source_today_update(self, url, source):
        index, doc_type = self.split_url(url)
        agg_time_field = 'update_time' if \
            index == 'judge_doc' or \
            index == 'executive_announcement' or \
            index == 'shixin_beizhixing' or \
            index == 'exposure_desk' else 'create_time'
        today = date.today()
        begin = today
        end = (today + timedelta(days=1))
        update_query = {
            "query": {
                "bool": {
                    "must": [{
                        "term": {
                            "source": {
                                "value": source
                            }
                        }
                    }, {
                        "range": {
                            agg_time_field: {
                                "gt": begin.isoformat(),
                                "lt": end.isoformat(),
                                "format": "yyyy-MM-dd"
                            }
                        }
                    }]
                }
            }
        }

        total_query = {
            "_source": "",
            "query": {
                "term": {
                    "source": {
                        "value": source
                    }
                }
            }
        }
        update_rst = self.es.search(
            index=index, doc_type=doc_type, body=update_query)
        total_rst = self.es.search(
            index=index, doc_type=doc_type, body=total_query)
        crawled_total = total_rst['hits']['total']
        crawled_update = update_rst['hits']['total']
        return {
            "source": source,
            "crawled_total": crawled_total,
            "crawled_update": crawled_update
        }

    def agg_day_by_source(self, url, source, begin=None, end=None):

        index, doc_type = self.split_url(url)
        agg_time_field = 'update_time' if \
            index == 'judge_doc' or \
            index == 'executive_announcement' or \
            index == 'shixin_beizhixing' or \
            index == 'exposure_desk' else 'create_time'
        if not begin and not end:
            begin = date(year=2016, month=1, day=1)
            end = date.today()

        query = {
            "size": 0,
            "query": {
                "bool": {
                    "must": [{
                        "range": {
                            agg_time_field: {
                                "gte": begin.isoformat(),
                                "lte": end.isoformat(),
                                "format": "yyyy-MM-dd"
                            }
                        }
                    }, {
                        "term": {
                            "source": {
                                "value": source
                            }
                        }
                    }]
                }
            },
            "aggs": {
                "create_time_agg": {
                    "date_histogram": {
                        "field": agg_time_field,
                        "interval": "day"
                    }
                }
            }
        }

        rst = self.es.search(index=index, doc_type=doc_type, body=query)
        result, _time = [], []
        for item in rst['aggregations']['create_time_agg']['buckets']:
            crawl_time = item['key_as_string']
            crawl_time = re.findall('(\d+)-(\d+)-(\d+)T', crawl_time)[0]
            crawl_time = date(
                year=int(crawl_time[0]),
                month=int(crawl_time[1]),
                day=int(crawl_time[2]))
            result.append({
                "crawl_time": crawl_time.isoformat(),
                "count": item['doc_count']
            })
            _time.append(crawl_time.isoformat())
        for d in range(1, int((end - begin).days) + 1):
            _d = (begin + timedelta(d)).isoformat()
            if _d not in _time:
                _time.append(_d)
                result.append({"crawl_time": _d, "count": 0})
        return sorted(result, key=lambda a: a['crawl_time'])


if __name__ == '__main__':
    esman = EsMan()
    today = date.today()
    end = today
    begin = today - timedelta(days=30)
    for item in esman.mapping('judge_doc/local_doc', source="裁判文书网"):
        print(item)
