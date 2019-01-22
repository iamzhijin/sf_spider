## rhinoAPI接口文档
___

> 创建时间: 2018-3-21



### 展示大屏API

#### 项目按日统计数量API
___
#### 接口简介
所有项目的每个爬虫某个时间段每天的数量展示
用于:
  - 展示大屏-数据更新趋势
  - 展示大屏-爬虫更新统计
  - 展示大屏-爬虫更新对比
  - 展示大屏-数据采集总量
___
#### 接口详情
__请求地址__    
```html
projects/crawls/count_by_day
```

__请求类型__  
GET    

__请求参数__    

| 参数名   | 类型   | 必填   | 描述   | 默认值  | 参考值       |
| ----- | ---- | ---- | ---- | ---- | --------- |
| begin | date | 是    | 开始时间 | -    | 2017-3-12 |
| end   | date | 是    | 结束时间 | -    | 2018-3-25 |

__返回正确JSON示例__

``` json
[
  {
    "project1": {
      "crawl1": {
        "day4": "num4",
        "day2": "num2",
        "day1": "num1",
        "day3": "num3"
      }
    }
  },
  {
    "project2": {
      "crawl1": {
        "day4": "num4",
        "day2": "num2",
        "day1": "num1",
        "day3": "num3"
      }
    }
  },
  {
    "project3": {
      "crawl1": {
        "day4": "num4",
        "day2": "num2",
        "day1": "num1",
        "day3": "num3"
      }
    }
  },
  {
    "project4": {
      "crawl1": {
        "day4": "num4",
        "day2": "num2",
        "day1": "num1",
        "day3": "num3"
      }
    }
  },
  {
    "project5": {
      "crawl1": {
        "day4": "num4",
        "day2": "num2",
        "day1": "num1",
        "day3": "num3"
      }
    }
  },
  {
    "project6": {
      "crawl1": {
        "day4": "num4",
        "day2": "num2",
        "day1": "num1",
        "day3": "num3"
      }
    }
  },
  {
    "project7": {
      "crawl1": {
        "day4": "num4",
        "day2": "num2",
        "day1": "num1",
        "day3": "num3"
      }
    }
  }
]

```

__返回错误JSON示例__
```json
{
  "code": 10500,
  "msg": "服务器未知报错"
}
```

__备注说明__　　
无



#### 接口简介

获得es爬取结果的总数和天数

#### 接口详情

__请求地址__

```html
project/crawls/total_count
```

__请求类型__    
GET  

__请求参数__    
无

__返回正确JSON示例__

```json
[
  {
  	"project1": {"count": "count", "days": "days"}
  },
   {
  	"project2": {"count": "count", "days": "days"}
  }
]
```

__返回错误JSON示例__

```json
{
  "code": 10500,
  "msg": "服务器未知报错"
}
```

__备注说明__　　
无






#### 爬虫总数API
#### 接口简介
从mysql查询爬虫总数量

#### 接口详情
__请求地址__

```HTML
crawls/total_count
```

__请求类型__    
GET  

__请求参数__    
无

__返回正确JSON示例__
```json
{
  "crawl_num": "crawl_num",
}
```
__返回错误JSON示例__
```json
{
  "code": 10500,
  "msg": "服务器未知报错"
}
```
__备注说明__　　
无



### 爬虫一览
#### 展示爬虫API
#### 接口简介
从mysql查询爬虫并展示在爬虫展示列表

#### 接口详情
__请求地址__

```HTML
crawls/info
```

__请求类型__    
GET  

__请求参数__    
| 参数名          | 类型   | 必填   | 描述    | 默认值  | 参考值          |
| ------------ | ---- | ---- | ----- | ---- | ------------ |
| name         | str  | 否    | 爬虫名称  | -    | 浙江高级人民法院开庭公告 |
| project_name | str  | 否    | 项目名称  | -    | 开庭公告         |
| crawl_owner  | str  | 否    | 爬虫负责人 | -    | 王枫           |
| status       | str  | 否    | 状态    | -    | 启动           |

__返回正确JSON示例__
```json
[
  {
  "update_today": "update_today",
  "project_name": "project_name",
  "update_by_day": "update_by_day",
  "status": "status",
  "web_url": "url",
  "create_time": "create_time",
  "total_count": "total_count",
  "crwal_count": "crawl_count",
  "crwal_name": "crwal_name",
  "need_date": "need_date"
	},
    {
  "update_today": "update_today",
  "project_name": "project_name",
  "update_by_day": "update_by_day",
  "status": "status",
  "web_url": "url",
  "create_time": "create_time",
  "total_count": "total_count",
  "crwal_count": "crawl_count",
  "crwal_name": "crwal_name",
  "need_date": "need_date"
	}
  ]
```
__返回错误JSON示例__
```json
{
  "code": 10500,
  "msg": "服务器未知报错"
}
```
__备注说明__　　
需要在crawler_manage_crwaler添加字段
| 参数名             | 类型   | 必填   | 描述    | 默认值  | 参考值                  |
| --------------- | ---- | ---- | ----- | ---- | -------------------- |
| web_title       | str  | 是    | 网站标题  | -    | 杭州法院公告               |
| web_url         | str  | 是    | 网站链接  | -    | http://www.baidu.com |
| update_strategy | str  | 是    | 更新策略  | -    | T+1                  |
| use_for         | str  | 否    | 使用场景  | -    | 检查                   |
| crawl_owner     | str  | 否    | 爬虫负责人 | -    | 陈磊                   |
| count           | int  | 否    | 预估数量  | -    | 3000000              |
| time_litmit     | int  | 否    | 要求时限  | -    | 156                  |

部分字段从es拿到



### 爬虫详情API

####　爬虫基本情况API

#### 接口简介
展示爬虫基本情况

#### 接口详情
__请求地址__

```HTML
crawl/base
```

__请求类型__    
GET  

__请求参数__    
| 参数名  | 类型   | 必填   | 描述   | 默认值  | 参考值          |
| ---- | ---- | ---- | ---- | ---- | ------------ |
| name | str  | 否    | 爬虫名称 | -    | 浙江高级人民法院开庭公告 |

__返回正确JSON示例__
```json
{
  "web_title": "网站名称",
  "web_url": "网站url",
  "crwal_name": "开庭公告",
  "count": "预估数量",
  "create_time": "起始日期",
  "use_for": "使用场景",
  "project_name": "开庭公告",
  "update_strategy": "更新策略",
  "time_litmit": "要求时限"
}
```
__返回错误JSON示例__
```json
{
  "code": 10500,
  "msg": "服务器未知报错"
}
```
__备注说明__　　
无



#### 更新爬虫基本信息API

#### 接口简介

更新爬虫信息的部分参数

#### 接口详情

__请求地址__

```html
crawl/base
```

__请求类型__    
POST  

__请求参数__    

| 参数名             | 类型   | 必填   | 描述   | 默认值  | 参考值     |
| --------------- | ---- | ---- | ---- | ---- | ------- |
| use_for         | str  | 否    | 使用场景 | -    | 检查      |
| update_strategy | str  | 否    | 更新策略 | -    | T+2     |
| count           | int  | 否    | 预估数量 | -    | 4000000 |
|                 |      |      |      |      |         |

__返回正确JSON示例__

```json
{
  "code": 10000,
  "msg": "更新成功"
}
```



__返回错误JSON示例__

```json
{
  "code": 10500,
  "msg": "服务器未知报错"
}
```

__备注说明__　　

无



#### 爬虫追踪状况API

#### 接口简介

返回项目数量情况

#### 接口详情

__请求地址__

```html
project/info
```

__请求类型__    
GET  

__请求参数__    

| 参数名          | 类型   | 必填   | 描述   | 默认值  | 参考值   |
| ------------ | ---- | ---- | ---- | ---- | ----- |
| crawl_name   | str  | 否    | 爬虫名称 | -    | 杭州曝光台 |
| project_name | str  | 否    | 项目名称 | -    | 开庭公告  |
|              |      |      |      |      |       |

__返回正确JSON示例__

```json
{
	"crwal_num":"crwal_num",
  	"complete_num": "complete_num",
  	"total_num": "total_num",
  	"complete_crawl": "complete_crawl"
}
```



__返回错误JSON示例__

```json
{
  "code": 10500,
  "msg": "服务器未知报错"
}
```

__备注说明__　　

无



#### 接口简介

返回爬虫数量情况

#### 接口详情

__请求地址__

```html
crwal/status
```

__请求类型__    
GET  

__请求参数__    

| 参数名        | 类型   | 必填   | 描述   | 默认值  | 参考值   |
| ---------- | ---- | ---- | ---- | ---- | ----- |
| crawl_name | str  | 否    | 爬虫名称 | -    | 杭州曝光台 |

__返回正确JSON示例__

```json
{
	"count":"count",
  	"crwaled_num": "crwaled_num",
  	"update_today": "update_today",
  	"status": "status"
}
```



__返回错误JSON示例__

```json
{
  "code": 10500,
  "msg": "服务器未知报错"
}
```

__备注说明__　　

无

#### 爬虫数量走势API

#### 接口简介

单个爬虫按日统计数量

#### 接口详情

__请求地址__

```html
crwal/count
```

__请求类型__    
GET  

__请求参数__    

| 参数名        | 类型   | 必填   | 描述   | 默认值  | 参考值   |
| ---------- | ---- | ---- | ---- | ---- | ----- |
| crawl_name | str  | 否    | 爬虫名称 | -    | 杭州曝光台 |

__返回正确JSON示例__

```json
{
  {
  	"day1": "num1",
    "day2": "num2",
    "day3": "num3",
    "day4": "num4",
    "day5": "num5",
    "day6": "num6"
  }
}
```



__返回错误JSON示例__

```json
{
  "code": 10500,
  "msg": "服务器未知报错"
}
```

__备注说明__　　

无



### 数据情况

通过es的API来展示

___



### 字段统计

#### 接口简介

单个爬虫按日统计数量

#### 接口详情

__请求地址__

```html
crwal/fields
```

__请求类型__    
GET  

__返回正确JSON示例__

```json
{
  {
  	"field1": "persent1",
    "field2": "persent1",
    "field3": "persent1",
    "field4": "persent1",
    "field5": "persent1",
    "field6": "persent1"
  }
}
```



__返回错误JSON示例__

```json
{
  "code": 10500,
  "msg": "服务器未知报错"
}
```

__备注说明__　　

无





