import pymysql

class Database():
    
    def __init__(self) -> None:
        # 数据库连接参数
        self.host = '00.00.00.00'
        self.user = 'root'
        self.password = '*********'
        self.database = 'bingxiang'
        self.connection = pymysql.connect(host=self.host, user=self.user, password=self.password, database=self.database)
    
    def quary_table(self):
        # 创建 cursor 对象
        with self.connection.cursor() as cursor:
            cursor.execute("SHOW TABLES")
                
                # 获取所有表名
            tables = cursor.fetchall()
            for table in tables:
                print(table)
        # 关闭连接
        
    #查询食品信息
    def quary_food(self):
        try:
            with self.connection.cursor() as cursor:
                sql = 'SELECT * FROM tb_food_info'
                cursor.execute(sql)
                
                results = cursor.fetchall()
                # for row in results:
                #     print(row)
        
        finally:
            return results

    #查询设备信息
    def quary_device(self):
        try:
            with self.connection.cursor() as cursor:
                len = cursor.rowcount
                if len < 5:
                    sql = 'SELECT * FROM tb_device_info'
                else:
                    sql = f'SELECT * FROM tb_device_info limit {len - 4} 5'#返回后行信息
                cursor.execute(sql)
                
                results = cursor.fetchall()
                # for row in results:
                #     print(row)
        
        finally:
            return results
    
    #录入食品信息
    def add_food(self,name,food_class=255, image = ' ',QR = ' '):
        try:
            with self.connection.cursor() as cursor:
                sql = 'INSERT INTO tb_food_info (name, class, image,QR,create_time, updata_time) VALUES (%s, %s, %s, %s,now(), now())' 
                data = (name, food_class, image, QR)
                
                cursor.execute(sql, data)
                
                self.connection.commit()
                print(f"成功修改 {cursor.rowcount} 条数据。")
        
        finally:
        #     self.connection.close()
            pass
        
    def del_food(self,index):
        try:
            with self.connection.cursor() as cursor:
                sql = "delete from tb_food_info where id = %s;" 
                data = (index)
                
                cursor.execute(sql, data)
                
                self.connection.commit()
                print(f"成功出库食品。")
        
        finally:
        #     self.connection.close()
            pass
    
    #录入设备信息
    def update_device(self, temperature=0, humidity=0, CO2=0):
        try:
            with self.connection.cursor() as cursor:
                sql = 'INSERT INTO tb_device_info (time, temperature, humidity, CO2) VALUES (now(), %s, %s ,%s)' 
                data = (temperature, humidity, CO2)
                
                cursor.execute(sql, data)
                
                self.connection.commit()
                print(f"成功修改 {cursor.rowcount} 条数据。")
        
        finally:
        #     self.connection.close()
            pass



if __name__ == '__main__':
    database = Database()
    # database.quary_table()
 
    # database.quary_device()
    # database.update_food('xianggua','1')
    # database.update_device()
    # database.del_food(index=3)
    a = database.quary_device()
    print(a[-1][0])
    
    database.connection.close()
        
