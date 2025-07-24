# 介绍

**数据库：**数据库是“按照数据结构来组织、存储和管理数据的仓库”。是一个长期存储在计算机内的、有组织的、可共享的、统一管理的大量数据的集合。

**应用场景：**在软件系统中无处不在，几乎所有的软件系统背后都有数据库，例如（淘宝，QQ，游戏等）。

**数据表展现形式：**

![001](images/001.PNG)

**主流关系型数据库：** SQL SERVER，MySQL，Oracle等。

**数据库的安装：（服务、管理工具）**

（1）在微软官网下载安装程序，https://www.microsoft.com/zh-cn/sql-server/sql-server-downloads

（2）百度搜索"I tell you"，或者访问 https://msdn.itellyou.cn/

![002](images/002.PNG)

**打开数据库：**

（1）启动服务：

​	【1】命令行启动；【2】SQL SERVER配置管理器；【3】Windows服务；

（2）打开SQL SERVER Management Studio，使用工具连接到数据库。

​	【1】Windows身份验证；	【2】SQL SERVER身份验证；

 **数据库基本操作：**

（1）建库。

（2）建表。

（3）数据维护。

**数据库的迁移：**

（1）数据库的分离、附加；（分离和删除的区别在于硬盘上是否还留存有数据库文件）

（2）数据库的备份，还原；

（3）数据库脚本的保存；

# 建库建表

## 一、检查数据库名是否存在

如果需要创建数据库，可能会出现数据库名字重名的现象，我们可以使用如下代码查询数据库名是否存在，存在则删除此数据库。

```sql
--删除数据库
if exists(select * from sys.databases where name = 'DBTEST')
	drop database DBTEST
```

此代码检查数据库中是否存在"DBTEST"数据库，如果存在则删除此数据库，此处理方式最好只在学习阶段使用，在正式生产环境中慎用，操作不当可能会删除重要数据。

## 二、创建数据库

```sql
--创建数据库
create database DBTEST
on  --数据文件
(
	name = 'DBTEST',   --逻辑名称
	filename = 'D:\Data\DBTEST.mdf',  -- 物理路径及名称
	size = 5MB,  -- 数据文件初始大小
	filegrowth = 2MB -- 数据文件增长速度,也可以使用百分比来设置
)
log on  --日志文件
(
	name = 'DBTEST_log', -- 逻辑名称
	filename = 'D:\Data\DBTEST_log.ldf', -- 物理路径及名称
	size = 5MB, -- 日志文件初始大小
	filegrowth = 2MB -- 日志文件增长速度,也可以使用百分比来设置
)
```

以上代码创建"DBTEST"数据库，并且分别使用on和log on规定了数据文件和日志文件的信息。

创建数据库也可以按照如下简单语法来创建：

```sql
create database DBTEST
```

如果按照上述方式创建数据库，数据库的数据文件和日志文件的相关信息，全部采取默认值。

## 三、建表

**使用数据库和删除数据表：**

```sql
use DBTEST  -- 切换当前数据库为DBTEST
-- 删除表(先判断表在当前数据库是否存在,存在则删除,其中type='U'判断对象类型为用户定义表类型)
if exists(select * from sys.objects where name = 'Department' and type = 'U')
	drop table Department
```

**创建数据表语法：**

```sql
create table 表名
(
	字段名1 数据类型(长度),
	字段名2 数据类型(长度)
)
```

其中数据类型，我们在后面用到什么类型，在介绍什么类型，有的类型可以不填写长度。

**创建数据表示例（部门表，职级表，员工信息表）：**

```sql
--创建部门表
create table Department -
(
	-- 创建部门编号;int代表整数类型;primary key代表主键;identity(1,1)代表从1开始步长为1自增长;
	DepartmentId int primary key identity(1,1),
	-- 创建部门名称;nvarchar(50)代表长度50的字符串;not null代表不能为空;
	DepartmentName nvarchar(50) not null,
	-- 创建部门描述；text代表长文本;
	DepartmentRemark text
)
```

**字符串类型比较：**

char：定长，例如 char(10)，不论你存储的数据是否达到了10个字节，都要占去10个字节的空间 。

varchar：变长，例如varchar(10)，并不代表一定占用10个字节，而代表最多占用10个字节。最大长度8000，也可以使用varchar(max)表示2G以内的数据，但存储机制会和text一样，效率会降低。

text：长文本， 最大长度为2^31-1(2,147,483,647)个字符 。

nchar,nvarchar,ntext：名字前面多了一个n， 它表示存储的是Unicode数据类型的字符，区别varchar(100)可以存储100个英文字母或者50个汉字，而nvarchar(100)可以存储100个英文字母，也可以存储100个汉字。

```sql
-- 创建职级表，rank为系统关键字，此处使用[]代表自定义名字，而非系统关键字，
-- 所以这句话的作用就是创建了一个名为[Rank]类型的表
create table [Rank]
(
	RankId int primary key identity(1,1),
	RankName nvarchar(50) not null,
	RankRemark text
)
```

```sql
--创建员工信息表
create table People
(
	PeopleId int primary key identity(1,1),
	-- references代表外键引用,此字段必须符合与其它表的外键约束
	DepartmentId int references Department(DepartmentId)  not null,
	RankId int references [Rank](RankId) not null,
	PeopleName nvarchar(50) not null,
	-- default代表字段默认值; check可以规定字段值的约束条件;
	PeopleSex nvarchar(1) default('男') check(PeopleSex='男' or PeopleSex='女') not null,
	PeopleBirth datetime not null,
	PeopleSalary decimal(12,2) check(PeopleSalary>= 1000 and PeopleSalary <= 100000) not null,
	-- unique代表唯一约束，为数据提供唯一性保证;
	PeoplePhone nvarchar(20) unique not null,
	PeopleAddress nvarchar(100),
	-- datetime和smalldatetime都可以表示时间类型，getdate()用于获取系统当前时间
	PeopleAddTime smalldatetime default(getdate())
)
```

# 修改表结构

 （1）如需在表中添加列，请使用下面的语法: 

```sql
ALTER TABLE table_name
ADD column_name datatype
```

例如该员工表添加一列员工邮箱：

```sql
alter table People
add PeopleMail nvarchar(100)
```

（2）如需在表中删除列，请使用下面的语法: 

```sql
ALTER TABLE table_name
DROP COLUMN column_name
```

例如删除员工表中的邮箱这一列

```sql
alter table People
drop column PeopleMail
```

（3）如需改变表中列的数据类型，请使用下列语法：

```sql
ALTER TABLE table_name
ALTER COLUMN column_name datatype
```

例如需要改变邮箱列的数据类型为varchar(100)

```sql
alter table People
alter column PeopleMail varchar(100)
```

## 五、删除添加约束

删除约束语法：

```sql
if exists(select * from sysobjects where name=约束名)
alter table 表名 drop constraint 约束名;
go
```

添加约束语法：

```sql
-- 添加主键约束
alter table 表名 add constraint 约束名称 primary key(列名)
-- 添加check约束
alter table 表名 add constraint 约束名称 check(条件表达式)
-- 添加unique约束
alter table 表名 add constraint 约束名称 unique(列名)
-- 添加default约束
alter table 表名 add constraint 约束名称 default 默认值 for 列名
-- 添加外键约束
alter table 表名 add constraint 约束名称 foreign key (列名) references 关联表名(关联表列名)
```

# 插入数据

## 一、向部门表插入数据

**标准语法：**

```sql
insert into Department(DepartmentName,DepartmentRemark)
values('软件部','......')
insert into Department(DepartmentName,DepartmentRemark)
values('硬件部','......')
insert into Department(DepartmentName,DepartmentRemark)
values('市场部','......')
```

**简写语法：（省略字段名称）**

```sql
insert into Department values('行政部','公司主管行政工作的部门')
```

此写法在给字段赋值的时候，必须保证顺序和数据表结构中字段顺序完全一致，不推荐使用此种写法，因为数据表结构变化的时候，数据会出错或产生错误数据。

**一次插入多行数据:**

```sql
insert into Department(DepartmentName,DepartmentRemark)
select '市场部','吹牛的部门' union
select '产品部','天马星空的部门' union
select '总经办','都是领导的部门' 
```

## 二、向职级表插入数据

```sql
insert into [Rank](RankName,RankRemark)
values('初级','辅助其他人完成任务')
insert into [Rank](RankName,RankRemark)
values('中级','具备独立处理事务的能力')
insert into [Rank](RankName,RankRemark)
values('高级','具备可以带动全场节奏的能力')
```

## 三、向员工表插入数据

```sql
insert into People(DepartmentId,RankId,PeopleName,PeopleSex,PeopleBirth,
PeopleSalary,PeoplePhone,PeopleAddress,PeopleAddTime)
values(1,3,'刘备','男','1984-7-9',20000,'13554785452','成都',getdate())

insert into People(DepartmentId,RankId,PeopleName,PeopleSex,PeopleBirth,
PeopleSalary,PeoplePhone,PeopleAddress,PeopleAddTime)
values(1,2,'孙尚香','女','1987-7-9',15000,'13256854578','荆州',getdate())

insert into People(DepartmentId,RankId,PeopleName,PeopleSex,PeopleBirth,
PeopleSalary,PeoplePhone,PeopleAddress,PeopleAddTime)
values(1,1,'关羽','男','1988-8-8',12000,'13985745871','荆州',getdate())

insert into People(DepartmentId,RankId,PeopleName,PeopleSex,PeopleBirth,
PeopleSalary,PeoplePhone,PeopleAddress,PeopleAddTime)
values(2,1,'张飞','男','1990-8-8',8000,'13535987412','宜昌',getdate())

insert into People(DepartmentId,RankId,PeopleName,PeopleSex,PeopleBirth,
PeopleSalary,PeoplePhone,PeopleAddress,PeopleAddTime)
values(2,3,'赵云','男','1989-4-8',9000,'13845789568','宜昌',getdate())

insert into People(DepartmentId,RankId,PeopleName,PeopleSex,PeopleBirth,
PeopleSalary,PeoplePhone,PeopleAddress,PeopleAddTime)
values(3,3,'马超','男','1995-4-8',9500,'13878562568','香港',getdate())

insert into People(DepartmentId,RankId,PeopleName,PeopleSex,PeopleBirth,
PeopleSalary,PeoplePhone,PeopleAddress,PeopleAddTime)
values(3,2,'黄盖','男','1989-4-20',8500,'13335457412','武汉',getdate())

insert into People(DepartmentId,RankId,PeopleName,PeopleSex,PeopleBirth,
PeopleSalary,PeoplePhone,PeopleAddress,PeopleAddTime)
values(3,1,'貂蝉','女','1989-4-20',6500,'13437100050','武汉',getdate())

insert into People(DepartmentId,RankId,PeopleName,PeopleSex,PeopleBirth,
PeopleSalary,PeoplePhone,PeopleAddress,PeopleAddTime)
values(2,2,'曹操','男','1987-12-20',25000,'13889562354','北京',getdate())

insert into People(DepartmentId,RankId,PeopleName,PeopleSex,PeopleBirth,
PeopleSalary,PeoplePhone,PeopleAddress,PeopleAddTime)
values(2,3,'许褚','男','1981-11-11',9000,'13385299632','北京',getdate())

insert into People(DepartmentId,RankId,PeopleName,PeopleSex,PeopleBirth,
PeopleSalary,PeoplePhone,PeopleAddress,PeopleAddTime)
values(2,1,'典韦','男','1978-1-13',8000,'13478545263','上海',getdate())

insert into People(DepartmentId,RankId,PeopleName,PeopleSex,PeopleBirth,
PeopleSalary,PeoplePhone,PeopleAddress,PeopleAddTime)
values(1,1,'曹仁','男','1998-12-12',7500,'13878523695','深圳',getdate())

insert into People(DepartmentId,RankId,PeopleName,PeopleSex,PeopleBirth,
PeopleSalary,PeoplePhone,PeopleAddress,PeopleAddTime)
values(1,3,'孙坚','男','1968-11-22',9000,'13698545841','广州',getdate())

insert into People(DepartmentId,RankId,PeopleName,PeopleSex,PeopleBirth,
PeopleSalary,PeoplePhone,PeopleAddress,PeopleAddTime)
values(3,3,'孙策','男','1988-1-22',11000,'13558745874','深圳',getdate())

insert into People(DepartmentId,RankId,PeopleName,PeopleSex,PeopleBirth,
PeopleSalary,PeoplePhone,PeopleAddress,PeopleAddTime)
values(3,2,'孙权','男','1990-2-21',12000,'13698745214','深圳',getdate())

insert into People(DepartmentId,RankId,PeopleName,PeopleSex,PeopleBirth,
PeopleSalary,PeoplePhone,PeopleAddress,PeopleAddTime)
values(3,2,'大乔','女','1995-2-21',13000,'13985478512','上海',getdate())

insert into People(DepartmentId,RankId,PeopleName,PeopleSex,PeopleBirth,
PeopleSalary,PeoplePhone,PeopleAddress,PeopleAddTime)
values(2,1,'小乔','女','1996-2-21',13500,'13778787874','北京',getdate())

insert into People(DepartmentId,RankId,PeopleName,PeopleSex,PeopleBirth,
PeopleSalary,PeoplePhone,PeopleAddress,PeopleAddTime)
values(1,2,'周瑜','男','1992-10-11',8000,'13987455214','武汉',getdate())

insert into People(DepartmentId,RankId,PeopleName,PeopleSex,PeopleBirth,
PeopleSalary,PeoplePhone,PeopleAddress,PeopleAddTime)
values(2,3,'鲁肃','男','1984-9-10',5500,'13254785965','成都',getdate())

insert into People(DepartmentId,RankId,PeopleName,PeopleSex,PeopleBirth,
PeopleSalary,PeoplePhone,PeopleAddress,PeopleAddTime)
values(3,3,'吕蒙','男','1987-5-19',8500,'13352197364','成都',getdate())

insert into People(DepartmentId,RankId,PeopleName,PeopleSex,PeopleBirth,
PeopleSalary,PeoplePhone,PeopleAddress,PeopleAddTime)
values(1,1,'陆逊','男','1996-5-19',7500,'13025457392','南京',getdate())

insert into People(DepartmentId,RankId,PeopleName,PeopleSex,PeopleBirth,
PeopleSalary,PeoplePhone,PeopleAddress,PeopleAddTime)
values(1,2,'太史慈','男','1983-6-1',7500,'13077778888','上海',getdate())
```

其中DepartmentId，RankId，PeopleSalary均为数字类型，在赋值的时候不需要添加单引号，而其它类型需要添加单引号。

## 四、查询数据是否插入成功

```sql
select * from Department
select * from [Rank]
select * from People 
```

# 关键字

* **ALTER PROCEDURE**: 修改已存在的存储过程

```sql
ALTER PROCEDURE [dbo].[PreGroup_GetPatientRY]` 表示要修改名为 `PreGroup_GetPatientRY` 的存储过程（属于 `dbo` 架构）

当存储过程已经存在时，使用 `ALTER PROCEDURE` 可以更新其定义（包括参数、SQL 逻辑等）

如果该存储过程不存在，执行此语句会报错（此时应使用 `CREATE PROCEDURE` 来创建新的存储过程）
```

* **AS**: 用于分隔定义与实现，明确标识 “声明部分” 与 “执行逻辑部分” 的边界

```sql
ALTER PROCEDURE [dbo].[PreGroup_GetPatientRY]
    -- 参数列表
AS
BEGIN
    -- 存储过程的执行逻辑
END
```

* **BEGIN**: 主要作用是定义代码块的开始，通常与 `END` 配合使用，用于将一组 SQL 语句组合成一个逻辑单元。

```sql
IF @IsSpecial=1
BEGIN
  -- 特殊用户的处理逻辑
END;
ELSE
BEGIN
  -- 普通用户的处理逻辑
END
```

**示例**

```sql
ALTER FUNCTION  [dbo].[Get_术种全院例次]
(	
	-- Add the parameters for the function here
	@出院起始日期 date,
	@出院结束日期 date
)
RETURNS TABLE 
AS
RETURN 
(
	SELECT 手术编码,SUM(例次) as 例次 from [dbo].[本院_手术例次月分布] 
	WHERE 年=YEAR(@出院起始日期) AND 月 BETWEEN MONTH(@出院起始日期) AND MONTH(@出院结束日期)
	GROUP BY 手术编码
)


ALTER FUNCTION [dbo].[Get_医院术种排名]
(	
	-- Add the parameters for the function here
	@出院起始日期 Datetime,
	@出院结束日期 date
)
RETURNS TABLE 
AS
RETURN 
(
	SELECT  手术编码,医院名称, SUM(例次) as 例次, RANK() OVER( partition BY 手术编码 ORDER BY SUM(例次) DESC,医院名称) AS 排名 	
	FROM 优劣势对比_术种例次
	WHERE 年=YEAR(@出院起始日期) AND 月 BETWEEN MONTH(@出院起始日期) AND MONTH(@出院结束日期)
	GROUP BY 手术编码,医院名称
)

ALTER FUNCTION [dbo].[Get_病种全院人次量]
(	
	-- Add the parameters for the function here
	@出院起始日期 Datetime,
	@出院结束日期 date
)
RETURNS TABLE 
AS
RETURN 
(
	SELECT 病种名称, SUM(CMI * 全院人次量)/NULLIF(sum(全院人次量),0) AS CMI, SUM(全院人次量) as 全院人次量  from [dbo].[本院_病种月分布] 
	WHERE convert ( datetime , convert ( varchar ,   年)+'-'+convert ( varchar , 月)+'-1'  ) between  @出院起始日期 and @出院结束日期
	group by 病种名称
)

ALTER FUNCTION [dbo].[Get_医院病种排名]
(	
	-- Add the parameters for the function here
	@出院起始日期 Datetime,
	@出院结束日期 date
)
RETURNS TABLE 
AS
RETURN 
(
	SELECT  病种名称,医院名称 , 人次量,排名  FROM (

	SELECT  病种名称,医院名称, SUM(人次量) as 人次量, row_number() OVER( partition BY 病种名称 ORDER BY SUM(人次量) DESC) AS 排名 	
	FROM 优劣势对比_病种人次
	WHERE convert ( datetime , convert ( varchar ,   年)+'-'+convert ( varchar , 月)+'-1'  ) between  @出院起始日期 and @出院结束日期
	group by 病种名称,医院名称
	
	
	) A 
)


```

