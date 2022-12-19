## Auto Test 框架 v2.0
> pytest + request + playwright +  allure 实现接口及ui自动化测试

简体中文 | [English](./README.en.md)

- 简易架构图

![IsXMnO.png](./1.png)


## 实现功能
- 接口直接的数据依赖: 需要B接口使用A接口响应中的某个字段作为参数
- 动态多断言： 可（多个）动态提取实际预期结果与指定的预期结果进行比较断言操作
- 支持sql查询断言
- 支持UI测试用例编写,基于po模式
- 重写源码page及context方法，支持会话保持
- 测试完成自动生成allure测试报告

## 目录结构
```shell
├─api
│  └─client.py	# API请求封装
├─config
│  └─config.yaml	# 配置文件
├─log
│  └─YYYY-MM-DD.log	# 日志文件
├─report
│  ├─data           # allure测试结果数据
│  └─html			      # allure报告
├─test-result       # 测试录屏结果输出路径
├─test
|  |
|  ├─API
|  | ├─conftest.py	# API测试初始化
|  | └─test_api.py	# 测试方法
|  └─UI
|    ├─conftest.py  # UI测试初始化
|    ├─test_case.yaml # UI测试案例，编写方法见文件说明
│    └─test_ui.py	  # 测试方法
|
├─tools		            # 工具包
│  ├─__init__.py		  # 常用方法封装
│  ├─data_process.py	# 依赖数据处理
|  ├─sql_operate.py   # 数据库操作
|  ├─email_send.py    # 邮件发送
|  ├─encode.py        # 接口加解密
|  ├─generate_data.py # 测试数据生成
|  └─read_file.py     # yaml文件获取封装
├─requirements.txt		# 项目依赖库文件
└─main.py	# 主启动文件
```

## 使用项目
1. 依赖安装 pip install -r requirements.txt
```shell
注： 如果需要移植的目标服务器无法联网 可以通过pip download -d packages/ -r requirements.txt 命令下载依赖包到当前目录的packages/文件夹中，目标服务器再通过 pip install --no-index --find-links=packages/ -r requirements.txt 离线安装依赖包
```

2. 创建如下mysql库表用于管理API测试用例
```
CREATE TABLE `Api_test_detail` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `CaseNo` varchar(128) NOT NULL COMMENT '用例编号',
  `Summary` varchar(128) NOT NULL COMMENT '用例概要描述',
  `Domain` varchar(128) NOT NULL COMMENT '域名或IP地址',
  `RquestHeader` varchar(128) DEFAULT NULL COMMENT '请求头',
  `InterfacePath` varchar(128) NOT NULL COMMENT '接口地址',
  `IsExecute` varchar(128) NOT NULL COMMENT '是否执行,Y是,N否',
  `Encode` varchar(128) NOT NULL COMMENT '是否调用加密接口加密入参,Y是N否',
  `MethodType` varchar(128) NOT NULL COMMENT '请求方法',
  `ParamsType` varchar(128) NOT NULL COMMENT '参数类型',
  `UploadFile` varchar(128) DEFAULT NULL COMMENT '上传的文件路径',
  `Params` longtext COMMENT '用例入参',
  `Sql` varchar(128) DEFAULT NULL COMMENT '断言的sql',
  `extract` varchar(128) DEFAULT NULL COMMENT '要提取的参数,jsonpath格式',
  `APIExpectResult` varchar(128) NOT NULL COMMENT '期望的api结果',
  `SqlExpectResult` varchar(128) DEFAULT NULL COMMENT '期望的sql结果',
  `add_time` datetime(6) NOT NULL COMMENT '创建时间',
  `update_time` datetime(6) NOT NULL COMMENT '更新时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
```
3. 编写测试用例
    测试用例使用数据库维护,需要配合测试平台使用,详见测试管理平台的使用

4. 创建如下库表用于记录测试结果及测试报告到数据库,用于测试管理平台获取报告并展示
```
CREATE TABLE `Api_test_result` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `total` int(11) NOT NULL COMMENT '用例总数',
  `passed` int(11) DEFAULT NULL COMMENT '通过数',
  `failed` int(11) DEFAULT NULL COMMENT '失败数',
  `error` int(11) DEFAULT NULL COMMENT '错误数',
  `skipped` int(11) DEFAULT NULL COMMENT '跳过数',
  `passed_rate` varchar(100) NOT NULL COMMENT '测试通过率',
  `report_path` varchar(128) DEFAULT NULL COMMENT '测试报告路径',
  `create_time` datetime NOT NULL COMMENT '创建时间',
  `update_time` datetime NOT NULL COMMENT '更新时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
```
6. UI测试用例编写
```
UI 测试用例编写指南
按照如下规范编写, 以关键字驱动测试执行
用例命名,为便于管理及美观整洁建议统一命名,如xxx(project)-xxx(mudule)-test001
descrption(用例描述)
test_step(测试步骤) 编写样例   test_step: { "open": "https://www.jd.com/",
                                "click1": "id=msShortcutLogin",
                                "fill1": {"selector": "#sb_form_q", "value": "test_account20221212"},
                                "swipe": {"x": 500, y: 800}
                                "sleep": 3000
                               }
支持的关键字有open(打开url), click1(点击事件,1则代表第一次点击,同理click2代表该测试用例中的第二次点击)
sleep(显式等待,使用毫秒),fill1(文本填充事件,需传入两个键值对,一个填充的元素对象,一个填充的值。数字1的用法与click1一致)
swipe(页面滑动事件)
expect_result(期望结果) 编写样例 {  "descrption": "期望页面"#header > span.text-header"元素的文案是'京东登录注册'",
                                   "selector": "#header > span.text-header",
                                    "value": "京东登录注册"
                                   }
```

5. 启用docker执行API自动化测试工具,执行 ```docker-compose up``` 开始构建并运行
(非docker部署方式可以执行  ```python main.py``` )

## jenkins集成
https://blog.csdn.net/weixin_45467232/article/details/123460355
