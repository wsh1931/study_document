# AOP

![img](.\images\1652151133261-9a474a6e-fa30-4b09-8cd1-7fba5e3ce92d.png)

连接点：所有方法

切入点：哪些方法需要追加功能的，匹配通知的方法，叫切入点

通知：各个方法共用的功能，叫通知。通知存在于通知类中。

切面：切面描述的是通知共用的功能与所对应切入点的关系。在哪些切入点上执行哪些通知叫切面

![img](.\images\1652151533449-8c75465e-38bf-491c-a973-a6c22fd93542.png)

![img](.\images\1652151558464-757f419d-f8bf-4416-bddb-21fa624a2925.png)

# AOP入门案例

![img](.\images\1652151763611-90780103-f14f-4357-a982-9131e05e895b.png)

```xml
1:pom.xml中导入坐标
```

![img](.\images\1652151893808-94074995-f7f7-4e89-b839-a45c90bfaaad.png)

```xml
3:制作共性功能，通知
```

![img](.\images\1652151972597-b89d9f70-e8ee-45af-9baf-c67197d1687e.png)

```xml
4:定义切入点
  在通知类中，定义一个空的private方法，在其上添加注解@Pointcut("execution(返回值类型 包名.类.方法)")

示例：
@Pointcut("execution(void com.itheima.dao.BookDao.update())")
private void pt(){}

在通知方法上，使用注解@Before("pt()")表示在pt()方法指向的切入点（com.itheima.dao.BookDao.update()）之前执行。
```

![img](.\images\1652152139116-8edca2d8-d6ec-40c4-9ece-fb50ead637eb.png)

![img](.\images\1652152379793-495c8316-fb81-4946-b82b-8165ae2ce78c.png)

```xml
5: 添加@Component 表示将该bean交给Spring
   添加@Aspect 表示该为AOP切面
```

![img](.\images\1652152535943-1632a931-b17a-4732-9ccd-5c96a5e92c7d.png)

```xml
6：在配置类中添加@EnableAspectJAutoProxy注解 

@EnableAspectJAutoProxy 启动了@Aspect 中的功能
@Aspect的功能是将切入点 通知定义好了
```

![img](.\images\1652152700861-d18cf351-8a1e-4fce-9b11-0800fdea0739.png)

## 入门案例总结

![img](.\images\1652152976978-5be6a0bd-55a8-43bc-93b0-4a323935752f.png)

![img](.\images\1652152994023-813d9b85-4da3-44a6-befb-8b53ef361910.png)

![img](.\images\1652153030803-a4476fe5-e3d8-4dc8-8005-a492ca2c78f0.png)

![img](.\images\1652153043261-f7e12e1a-cf10-4f6b-a84c-bc5cb3f0fc2f.png)

![img](.\images\1652153103033-62fedcb0-1afd-429f-a6db-7e0a8d970a16.png)

![img](.\images\1652153183538-a09043da-32bd-429f-8187-b18b967bf199.png)

![img](.\images\1652153200960-a077a40e-781a-47bb-9fdd-685ce3b96df1.png)



# AOP工作流程

```xml
1: Spring容器启动
2：读取所有切面配置中的切入点
  （截图中黄色部分，虽然ptx()方法也做了切入点@Pointcut,但是下面并没有声明通知类型 
   比如 @Before("方法（）")）
```

![img](.\images\1652161889124-a3eb6fa9-cb74-4364-bee2-27cb41846784.png)

![img](.\images\1652163765056-77a98e5d-7fd2-45df-9270-8b37ab767008.png)

![img](.\images\1652164513264-a249d39e-66cc-4f7b-80e2-7cbdde44b1bd.png)

![img](.\images\1652164528012-b1b447c1-2af2-4b8c-bfbb-17c3f85e1ec5.png)

# AOP切入点表达式

![img](.\images\1652164717902-ad1bb35c-a898-4ab9-bc4e-0dfd851f3a86.png)

![img](.\images\1652165025853-a0196a49-f7e5-4f0d-b884-eeb917af93dc.png)

![img](.\images\1652165547517-bd780903-8c6f-4186-9370-83cd6c745000.png)

![img](.\images\1652166196191-45917b36-af77-48a7-88c2-5dff14089315.png)

# AOP通知类型

![img](.\images\1652166958367-678f0bd8-84e6-4695-ac1a-1c586dec3593.png)

![img](.\images\1652167284969-a003534e-231d-45eb-bf46-6ff3a469c44f.png)

环绕通知

![img](.\images\1652168059586-bba9dc6e-91c6-40f3-a48a-d3524b57e738.png)

返回后通知：发生异常之后，不会运行

![img](.\images\1652169879688-99467267-bca1-46bc-a60a-fa8b65b20ee1.png)



![img](.\images\1652169966645-5cca43f4-5b08-45e2-aafd-7f0681878d7d.png)

![img](.\images\1652170003254-fb1cb130-7733-4d1a-8420-e70ab42d48fa.png)

![img](.\images\1652170016141-3e3324ad-c86c-4664-93a3-6710fee2213c.png)

![img](.\images\1652170073210-819d0bc8-a49e-42c4-932e-5860ab564e16.png)

![img](.\images\1652170197177-2d0807f8-416b-4a83-b84c-eed64e17a2d9.png)

![img](.\images\1652170212520-e0674080-a761-4027-bc37-41d5dfa61327.png)

![img](.\images\1652170233926-0f5b2a2e-1bd5-41a2-8f6b-e7faf523b7e5.png)

写一个通知类的步骤

```java
1: @Component
2: @Aspect
定义的一个通知类

3: @Ponitcut("execution(返回值类型 包.方法(参数))")
定义的通知空方法

4：@Around("类名.通知空方法()")
定义加强的通知方法
public Object runSpeed(ProceedingJoinPoint pjp){
    
    Objection ret = pjp.proceed();
    return ret;
}
```

![img](.\images\1652200990320-f1ef04f4-8eb8-4524-9b04-2d09f30de21a.png)

# AOP通知获取数据

![img](.\images\1652201371356-b4424341-e6f4-49a1-9e35-b0168bd63888.png)

![img](.\images\1652280471471-56dc800f-d100-49f2-b321-f7cb451fd222.png)

```java
//注解中的returing和形参需要保持一致
@AfterReturing(value = "pt()",returing="ret")
public void afterReturning(String ret){
    
}
```

![img](.\images\1652280538027-cf158f60-d1c1-4bdf-8d9a-89c9958ccaf8.png)

![img](.\images\1652280573703-b2f881c8-1487-457d-80f3-9c3e577d2ab2.png)

![img](.\images\1652280723836-ffe6103d-cb02-4a6f-87c7-42651ded8cef.png)

# 案例-百度网盘密码数据兼容处理

![img](.\images\1652281490861-0904a0ec-0800-49e5-9753-1d32824cbf6e.png)

# AOP总结

![img](.\images\1652281619020-f283be4b-f995-45f9-8766-316a8068dca3.png)

![img](.\images\1652281763821-fcca8c96-c358-48ff-8dcc-e9c3dc64a94b.png)

![img](.\images\1652281775546-c15e7a4c-92b3-4941-b681-415e8c73a4ab.png)

![img](.\images\1652281833120-b71ef6a8-227e-4080-8705-62ae3b4dde8c.png)

![img](.\images\1652281949054-95cdc83f-88e0-465d-96e6-3a727f3a358a.png)

![img](.\images\1652281986922-2ac7dede-d398-4bfc-abc9-2af80649f3df.png)

