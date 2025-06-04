# 大数据集群计算原理与编程课程设计

# Big Data Cluster Computing

## 项目简介
这是一个关于大数据集群计算的项目，旨在通过Django框架实现一个基于Web的应用程序，用于处理和分析大数据集群中的数据。项目包括数据读取、预处理、分布式计算等功能。

## 项目结构
```
DjangoProject/
├── .idea/
├── DjangoProject/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── db.sqlite3
├── manage.py
├── myfile/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── hdfs_config.py
│   ├── models.py
│   ├── tests.py
│   └── views.py
├── preprocessing/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── process.py
│   ├── tests.py
│   └── views.py
├── readfile/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── management/
│   │   ├── commands/
│   │   │   ├── filetype_count.py
│   │   │   └── __init__.py
│   ├── models.py
│   ├── tests.py
│   └── views.py
└── your_app/
    ├── __init__.py
    ├── management/
    │   ├── __init__.py
    │   ├── commands/
    │   │   ├── test_hdfs.py
    │   │   └── __init__.py
    ├── utils/
    │   ├── hdfs_client.py
    │   └── __init__.py
    ├── models.py
    ├── tests.py
    └── views.py
```

## 安装与运行
### 前提条件
- Python 3.12
- Django 4.x
- Git

## 功能介绍
- **数据读取**：通过 `readfile` 应用程序读取HDFS上的数据文件。
- **数据预处理**：在 `preprocessing` 应用程序中实现数据的清洗、转换等功能。
- **分布式计算**：利用Hadoop和MapReduce框架进行分布式计算，支持大规模数据处理。

## 使用说明
### 测试集群连接
   ```bash
   python manage.py test_hdfs
   ```

### 数据预处理
1. 在 `preprocessing` 应用程序中定义预处理逻辑。
2. 调用 `process.py` 中的函数进行数据处理。

### HDFS文件统计分布式计算
   
   ```bash
   # 统计根目录文件类型
   python manage.py filetype_count
   # 统计指定目录（示例：/user/data）
   python manage.py filetype_count --path /user/data
   ```

### 创建其他模块应用
   
   ```bash
   # 创建模块应用
   python manage.py startapp xxx
   # 之后需要在setting.py当中添加
   ```
