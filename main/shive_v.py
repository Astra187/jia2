import configparser
import re
import json
import os
import mysql.connector
from django.http import JsonResponse
from hdfs import InsecureClient
from pyhive import hive
import csv
from util.configread import config_read
from util.CustomJSONEncoder import CustomJsonEncoder
from util.codes import normal_code, system_error_code
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, date_format
import shutil
# 获取当前文件路径的根目录
parent_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

m_username = "26983"
hadoop_client = InsecureClient('http://localhost:9870', user='hadoop')

dbtype, host, port, user, passwd, dbName, charset,hasHadoop = config_read(os.path.join(parent_directory,"config.ini"))

#将mysql里的相关表转成hive库里的表
def migrate_to_hive():

    mysql_conn = mysql.connector.connect(
        host=host,
        port=port,
        user=user,
        password=passwd,
        database=dbName
    )
    cursor = mysql_conn.cursor()

    hive_conn = hive.Connection(
        host='localhost',
        port=10000,
        username=m_username,
    )
    hive_cursor = hive_conn.cursor()
    #创建Hive数据库（如果不存在）
    hive_cursor.execute(f"CREATE DATABASE IF NOT EXISTS {dbName}")
    hive_cursor.execute(f"USE {dbName}")

    musicinfo_table_path=f'/user/hive/warehouse/{dbName}.db/musicinfo'
    #删除已有的hive表
    if hadoop_client.status(musicinfo_table_path,strict=False):
        hadoop_client.delete(musicinfo_table_path, recursive=True)
    # 在Hive中删除表
    musicinfo_drop_table_query = f"""DROP TABLE musicinfo"""
    hive_cursor.execute(musicinfo_drop_table_query)
    cursor.execute("SELECT * FROM musicinfo")
    musicinfo_column_info = cursor.fetchall()
    #将数据写入 CSV 文件
    musicinfo_path = os.path.join(parent_directory, "musicinfo.csv")
    with open(musicinfo_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        # 写入数据行
        for row in musicinfo_column_info:
            writer.writerow(row)
    musicinfo_spakr_clear(musicinfo_path)
    cursor.execute("DESCRIBE musicinfo")
    musicinfo_column_info = cursor.fetchall()
    create_table_query = "CREATE TABLE IF NOT EXISTS musicinfo ("
    for column, data_type, _, _, _, _ in musicinfo_column_info:
        match = re.match(r'(\w+)(\(\d+\))?', data_type)
        mysql_type = match.group(1)
        hive_data_type = get_hive_type(mysql_type)
        create_table_query += f"{column} {hive_data_type}, "
    musicinfo_create_table_query = create_table_query[:-2] + ") row format delimited fields terminated by ','"
    hive_cursor.execute(musicinfo_create_table_query)
    # 上传映射文件
    musicinfo_hdfs_csv_path = f'/user/hive/warehouse/{dbName}.db/musicinfo'
    hadoop_client.upload(musicinfo_hdfs_csv_path, musicinfo_path)
    cursor.close()
    mysql_conn.close()
    hive_cursor.close()
    hive_conn.close()

#转换成hive的类型
def get_hive_type(mysql_type):
    type_mapping = {
        'INT': 'INT',
        'BIGINT': 'BIGINT',
        'FLOAT': 'FLOAT',
        'DOUBLE': 'DOUBLE',
        'DECIMAL': 'DECIMAL',
        'VARCHAR': 'STRING',
        'TEXT': 'STRING',
    }
    if isinstance(mysql_type, str):
        mysql_type = mysql_type.upper()
    return type_mapping.get(str(mysql_type), 'STRING')

#执行hive查询
def hive_query():
    # 连接到Hive服务器
    conn = hive.Connection(host='localhost', port=10000, username=m_username,database=dbName)
    # 创建一个游标对象
    cursor = conn.cursor()
    try:

        #定义Hive查询语句
        songname_query = "SELECT COUNT(*) AS total, songname FROM musicinfo GROUP BY songname"
        # 执行Hive查询语句
        cursor.execute(songname_query)
        # 获取查询结果
        songname_results = cursor.fetchall()
        songname_json_list=[]
        for row in songname_results:
            songname_json_list.append({"songname":row[1],"total":row[0]})
        #将JSON数据写入文件
        with open(os.path.join(parent_directory, "musicinfo_groupsongname.json"), 'w', encoding='utf-8') as f:
            json.dump(songname_json_list, f, ensure_ascii=False, indent=4)


        #定义Hive查询语句
        songstyle_query = "SELECT COUNT(*) AS total, songstyle FROM musicinfo GROUP BY songstyle"
        # 执行Hive查询语句
        cursor.execute(songstyle_query)
        # 获取查询结果
        songstyle_results = cursor.fetchall()
        songstyle_json_list=[]
        for row in songstyle_results:
            songstyle_json_list.append({"songstyle":row[1],"total":row[0]})
        #将JSON数据写入文件
        with open(os.path.join(parent_directory, "musicinfo_groupsongstyle.json"), 'w', encoding='utf-8') as f:
            json.dump(songstyle_json_list, f, ensure_ascii=False, indent=4)

        where = ' WHERE 1 = 1 '
        songname_query = f'''SELECT `songname`, ROUND(SUM(`playcount`), 2) AS `total`
            FROM musicinfo {where} GROUP BY `songname`'''
        #执行Hive查询语句
        cursor.execute(songname_query)
        # 获取查询结果
        songname_results = cursor.fetchall()
        songname_json_list=[]
        for row in songname_results:
            songname_json_list.append({"songname":row[0],"total":row[1]})
        #将JSON数据写入文件
        with open(os.path.join(parent_directory, "musicinfo_valuesongnameplaycount.json"), 'w', encoding='utf-8') as f:
            json.dump(songname_json_list, f, ensure_ascii=False, indent=4)
        where = ' WHERE 1 = 1 '
        songname_query = f'''SELECT `songname`, ROUND(SUM(`sharecount`), 2) AS `total`
            FROM musicinfo {where} GROUP BY `songname`'''
        #执行Hive查询语句
        cursor.execute(songname_query)
        # 获取查询结果
        songname_results = cursor.fetchall()
        songname_json_list=[]
        for row in songname_results:
            songname_json_list.append({"songname":row[0],"total":row[1]})
        #将JSON数据写入文件
        with open(os.path.join(parent_directory, "musicinfo_valuesongnamesharecount.json"), 'w', encoding='utf-8') as f:
            json.dump(songname_json_list, f, ensure_ascii=False, indent=4)
        where = ' WHERE 1 = 1 '
        songname_query = f'''SELECT `songname`, ROUND(SUM(`commentcount`), 2) AS `total`
            FROM musicinfo {where} GROUP BY `songname`'''
        #执行Hive查询语句
        cursor.execute(songname_query)
        # 获取查询结果
        songname_results = cursor.fetchall()
        songname_json_list=[]
        for row in songname_results:
            songname_json_list.append({"songname":row[0],"total":row[1]})
        #将JSON数据写入文件
        with open(os.path.join(parent_directory, "musicinfo_valuesongnamecommentcount.json"), 'w', encoding='utf-8') as f:
            json.dump(songname_json_list, f, ensure_ascii=False, indent=4)
        pass
    except Exception as e:
         print(f"An error occurred: {e}")
    finally:
        # 关闭游标和连接
        cursor.close()
        conn.close()

#spark数据清洗和预处理
def musicinfo_spakr_clear(csvpath):
    try:
        #创建Spark会话
        spark = SparkSession.builder.appName("tingge1eg9z2w5").getOrCreate()
        df = spark.read.csv(csvpath, header=False, inferSchema=True)
        df = df.toDF(
            "id",
            "addtime",
            "songname",
            "songstyle",
            "singer",
            "albumtitle",
            "imgurl",
            "playcount",
            "author",
            "favcount",
            "sharecount",
            "commentcount",
            "songcount",
            "playlist",
            "durtime",
            "albumdesc",
            "detailurl",
            "clicktime",
            "discussnum",
            "storeupnum",
        )
        #显示原始数据
        df.show()
        #1.删除空值
        df_cleaned = df.dropna()
        #2.去除重复行
        df_cleaned = df_cleaned.dropDuplicates()
        df_cleaned = df_cleaned.withColumn("addtime", date_format(col("addtime"), 'yyyy-MM-dd HH:mm:ss'))
        df_cleaned = df_cleaned.withColumn("clicktime", date_format(col("clicktime"), 'yyyy-MM-dd HH:mm:ss'))
        #显示清洗后的数据
        df_cleaned.show()
        #保存清洗后的数据
        print(type(df_cleaned))
        output_path = 'musicinfo_output_dir'  # 输出的目录
        df_cleaned.coalesce(1).write.csv(output_path, header=False, mode="overwrite")
        #手动移动生成的 CSV 文件到目标路径，并重命名
        for filename in os.listdir(output_path):
            if filename.startswith("part-") and filename.endswith(".csv"):
                shutil.move(os.path.join(output_path, filename), csvpath)
        #清理临时目录
        shutil.rmtree(output_path)
        #停止Spark会话
        spark.stop()
    except Exception as e:
        print("e:",e)
    # hive分析
def shive_analyze(request):
    if request.method in ["POST", "GET"]:
        msg = {"code": normal_code, "msg": "成功", "data": {}}
        try:
            migrate_to_hive()
            hive_query()
            return JsonResponse(msg, encoder=CustomJsonEncoder)
        except Exception as e:
            msg['code'] = system_error_code
            msg['msg'] = f"发生错误：{e}"
            return JsonResponse(msg, encoder=CustomJsonEncoder)



