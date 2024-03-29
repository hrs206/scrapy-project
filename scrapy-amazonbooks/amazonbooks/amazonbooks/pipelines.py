# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import mysql.connector

class AmazonbooksPipeline:
    def __init__(self) -> None:
        self.create_connection()
        self.create_table()
    
    def create_connection(self):
        self.conn = mysql.connector.connect(
            host = "localhost",
            user = "root",
            passwd = "password",
            database = "amazonbooks"
        )
        self.curr = self.conn.cursor()
    
    def create_table(self):
        self.curr.execute("""DROP TABLE IF EXISTS data""")
        self.curr.execute("""create table data(
                            title varchar(300),
                            rating varchar(50),
                            price int
                            )""")

    def process_item(self, item, spider):
        self.store_db(item)
        return item
    
    def store_db(self, item):
        self.curr.execute("""insert into data values (%s, %s, %s)""", 
                          (item["title"],
                          item["rating"],
                          item["price(INR)"]))
        self.conn.commit()
