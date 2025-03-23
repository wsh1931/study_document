# 注解

## 注解入门

![什么是注解](.\images\1.png)

```java
//什么是注解
public class Demo01_Annotation extends Object {
    //@Override就是一个注解
    @Override
    public String toString() {
        return super.toString();
    }
}
```

## 内置注解



![image-20210216173225256](.\images\2.png)



```java
// 什么是注解
public class Demo01_Annotation extends Object {
    // @Override就是一个注解
    @Override
    public String toString() {
        return super.toString();
    }

    // @Deprecated不推荐程序员使用,但是可以使用,或者存在更好的更新方式
    @Deprecated
    public static void test() {
        System.out.println("Deprecated");
    }

    // @SuppressWarnings 镇压警告
    @SuppressWarnings("all")
    public void test01(){
        List<String> list = new ArrayList<String>();
    }

    public static void main(String[] args) {
        test();
    }
}
```



## 自定义注解,元注解

![image-20210216180713223](.\images\3.png) 

```java
//测试元注解
@MyAnnotation
public class Demo02_MetaAnnotation {
    @MyAnnotation
    public void test() {

    }
}

//定义一个注解
//@Target可以用在什么地方
//ElementType.METHOD方法上有效  ElementType.TYPE类上有效
@Target(value = {ElementType.METHOD, ElementType.TYPE})
//@Retention在什么地方有效
//RUNTIME>CLASS>SOURCES
@Retention(value = RetentionPolicy.RUNTIME)
//@Documented 表示是否将我们的注解生成在Javadoc中
@Documented
//@Inherited 子类可以继承父类的注解
@Inherited
@interface MyAnnotation { }
```

![image-20210216182116415](D:\Typora\images\4.png)

```java
//自定义注解
public class Demo03_CustomAnnotation {
    //注解可以显示赋值,如果没有默认值,就必须给注解赋值
    @MyAnnotation2(name = "张三")
    public void test() {
    }
}

@Target(value = {ElementType.TYPE, ElementType.METHOD})
@Retention(RetentionPolicy.RUNTIME)
@interface MyAnnotation2 {
    //注解的参数:参数类型+参数名()
    //String name();
    String name() default "";
    int age() default 0;
    int id() default -1;//-1代表不存在
    String[] schools() default {"西部开源","清华大学"};

```

# 反射机制

## Java反射机制概念

### 静态 & 动态语言

![image-20210216184313269](.\images\5.png)

### 反射机制概念

![image-20210216184924651](.\images\6.png)

### 反射机制研究与应用

![image-20210216185137513](.\images\7.png)

### 反射机制优缺点

![image-20210216185230072](.\images\8.png)

![image-20210216185326797](.\images\9.png)

### 实现

```java
//什么叫反射
public class Demo04_Reflection {
    public static void main(String[] args) throws ClassNotFoundException {
        // 通过反射获取类的class对象
        Class<?> c = Class.forName("cn.doris.reflection.User");
        System.out.println(c);
        Class<?> c1 = Class.forName("cn.doris.reflection.User");
        Class<?> c2 = Class.forName("cn.doris.reflection.User");
        Class<?> c3 = Class.forName("cn.doris.reflection.User");
        Class<?> c4 = Class.forName("cn.doris.reflection.User");
        // 一个类在内存中只有一个Class对象
        // 一个类被加载后,类的整个结构都会被封装在Class对象中
        /**
         * public native int hashCode();返回该对象的hash码值
         * 	注：哈希值是根据哈希算法算出来的一个值，这个值跟地址值有关，但不是实际地址值。
         */
        System.out.println(c1.hashCode());
        System.out.println(c2.hashCode());
        System.out.println(c3.hashCode());
        System.out.println(c4.hashCode());
    }
}

//实体类
class User {
    private String name;
    private int id;
    private int age;

    public User() {
    }

    public User(String name, int id, int age) {
        this.name = name;
        this.id = id;
        this.age = age;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public int getId() {
        return id;
    }

    public void setId(int id) {
        this.id = id;
    }

    public int getAge() {
        return age;
    }

    public void setAge(int age) {
        this.age = age;
    }
}
```

## 理解Class类并获取Class实例

### class类介绍

![image-20210216190910198](.\images\10.png)

![image-20210216191140821](.\images\11.png)

![image-20210216191422819](.\images\13.png)

### 获取Class类的实例

![image-20210216191541455](.\images\12.png)

```java
//测试class类的创建方式有哪些
public class Demo05_CreateClass {
    public static void main(String[] args) throws ClassNotFoundException {
        Person person = new Student();
        System.out.println("这个人是:"+person.name);

        //方式一:通过对象查询
        Class c1 = person.getClass();
        System.out.println(c1.hashCode());

        //方式二:forname获得
        Class c2 = Class.forName("cn.doris.reflection.Student");
        System.out.println(c2.hashCode());

        //方式三:通过类名.class获得
        Class c3 = Student.class;
        System.out.println(c3.hashCode());

        //方式四,基本类型的包装类都有一个Type
        Class c4 = Integer.TYPE;
        System.out.println(c4);

        //获得父类类型
        Class c5 = c1.getSuperclass();
        System.out.println(c5);

    }
}

class Person {
    String name;

    public Person() {
    }

    public Person(String name) {
        this.name = name;
    }

    @Override
    public String toString() {
        return "Person{" +
                "name=" + name +
                '}';
    }
}

class Student extends Person {
    public Student() {
        this.name = "学生";
    }
}

class Teacher extends Person {
    public Teacher() {
        this.name = "老师";
    }
}
```

### 哪些类型可以有Class对象

![image-20210216192745039](.\images\14.png)

```java
//所有类型的Class
public class Demo06_AllTypeClass {
    public static void main(String[] args) {
        Class c1 = Object.class; //类
        Class c2 = Comparable.class; //接口
        Class c3 = String[].class; //一维数组
        Class c4 = int[][].class; //二维数组
        Class c5 = Override.class; //注解
        Class c6 = ElementType.class; //美剧
        Class c7 = Integer.class; //基本数据类型
        Class c8 = void.class; //void
        Class c9 = Class.class; //class
        System.out.println(c1);
        System.out.println(c2);
        System.out.println(c3);
        System.out.println(c4);
        System.out.println(c5);
        System.out.println(c6);
        System.out.println(c7);
        System.out.println(c8);
        System.out.println(c9);

        //只要元素类型与维度一样,就是同一个Class
        int[] a = new int[10];
        int[] b = new int[100];
        System.out.println(a.getClass().hashCode());
        System.out.println(b.getClass().hashCode());
    }
}
```

## 类的加载与ClassLoader

### Java内存分析

![image-20210216194320837](.\images\15.png)

### 类的加载

![image-20210216194443232](.\images\16.png)

![image-20210216194522442](.\images\17.png)

深刻理解类加载:https://blog.csdn.net/m0_38075425/article/details/81627349

```java
//类加载
public class Demo07_ClassLoader {
    public static void main(String[] args) {
        A a = new A();
        System.out.println(A.m);
        /**
         * 1. 加载到内存,会产生一个类对应Class对象
         * 2. 链接,连接结束后m=0
         * 3. 初始化
         *  <clinit>(){
         *       System.out.println("A类静态代码块初始化");
         *       m = 300;
         *       m = 100;
         *  }
         */
    }
}

class A {
    static {
        System.out.println("A类静态代码块初始化");
        m = 300;
    }

    static int m = 100;

    public A() {
        System.out.println("A类无参构造初始化");
    }
}
```

分析上面代码

![image-20210216200336439](.\images\18.png)

程序自上往下执行

### 什么时候会发生类初始化

![image-20210216201156532](.\images\19.png)

```java
//测试类什么时候会初始化
public class Demo08_ActiveReference {
    static {
        System.out.println("Main类被加载");
    }
    public static void main(String[] args) throws ClassNotFoundException {
        // 1. 主动调用
        //Son son = new Son();

        // 反射也会产生主动引用
        //Class.forName("cn.doris.reflection.Son");

        //不会产生类的引用的方法
        //System.out.println(Son.b);

        //Son[] array = new Son[5];
        
        //System.out.println(Son.a);
    }
}

class Father {
    static final int b = 2;
    static {
        System.out.println("父类被加载");
    }
}
class Son extends Father {
    static {
        System.out.println("子类被加载");
        m = 100;
    }
    static int m = 300;
    static final int a = 1;
}
```

### 类加载器的作用

![image-20210216202554642](.\images\20.png)

![image-20210216202736261](.\images\21.png)

> ClassLoader systemClassLoader = ClassLoader.getSystemClassLoader();//获取系统类的加载器
>
> ClassLoader parent = systemClassLoader.getParent();//获取系统类加载器的父类加载器-->扩展类加载器    jre1.8.0_91\lib\ext
>
> ClassLoader parent1 = parent.getParent();//获取扩展类加载器父类加载器-->根加载器(c/c++)  jre1.8.0_91\lib\rt.jar

```java
//类加载器
public class Demo09_ClassLoader1 {
    public static void main(String[] args) throws ClassNotFoundException {
        //获取系统类的加载器
        ClassLoader systemClassLoader = ClassLoader.getSystemClassLoader();
        System.out.println(systemClassLoader);

        //获取系统类加载器的父类加载器-->扩展类加载器    jre1.8.0_91\lib\ext
        ClassLoader parent = systemClassLoader.getParent();
        System.out.println(parent);

        //获取扩展类加载器父类加载器-->根加载器(c/c++)  jre1.8.0_91\lib\rt.jar
        ClassLoader parent1 = parent.getParent();
        System.out.println(parent1);

        //测试当前类是哪个加载器加载的
        ClassLoader classLoader = Class.forName("cn.doris.reflection.Demo09_ClassLoader1").getClassLoader();
        System.out.println(classLoader);

        //测试JDK内置的类是谁加载的
        classLoader = Class.forName("java.lang.Object").getClassLoader();
        System.out.println(classLoader);

        //如何获得系统类加载器可以加载的路径
        System.out.println(System.getProperty("java.class.path"));

        //双亲委派机制  检测安全性 你写的类和跟加载器一样的不会用你写的类
            //java.lang.String -->往上推


        /**
         * D:\Environment\java\jdk1.8.0_91\jre\lib\charsets.jar;
         * D:\Environment\java\jdk1.8.0_91\jre\lib\deploy.jar;
         * D:\Environment\java\jdk1.8.0_91\jre\lib\ext\access-bridge-64.jar;
         * D:\Environment\java\jdk1.8.0_91\jre\lib\ext\cldrdata.jar;
         * D:\Environment\java\jdk1.8.0_91\jre\lib\ext\dnsns.jar;
         * D:\Environment\java\jdk1.8.0_91\jre\lib\ext\jaccess.jar;
         * D:\Environment\java\jdk1.8.0_91\jre\lib\ext\jfxrt.jar;
         * D:\Environment\java\jdk1.8.0_91\jre\lib\ext\localedata.jar;
         * D:\Environment\java\jdk1.8.0_91\jre\lib\ext\nashorn.jar;
         * D:\Environment\java\jdk1.8.0_91\jre\lib\ext\sunec.jar;
         * D:\Environment\java\jdk1.8.0_91\jre\lib\ext\sunjce_provider.jar;
         * D:\Environment\java\jdk1.8.0_91\jre\lib\ext\sunmscapi.jar;
         * D:\Environment\java\jdk1.8.0_91\jre\lib\ext\sunpkcs11.jar;
         * D:\Environment\java\jdk1.8.0_91\jre\lib\ext\zipfs.jar;
         * D:\Environment\java\jdk1.8.0_91\jre\lib\javaws.jar;
         * D:\Environment\java\jdk1.8.0_91\jre\lib\jce.jar;
         * D:\Environment\java\jdk1.8.0_91\jre\lib\jfr.jar;
         * D:\Environment\java\jdk1.8.0_91\jre\lib\jfxswt.jar;
         * D:\Environment\java\jdk1.8.0_91\jre\lib\jsse.jar;
         * D:\Environment\java\jdk1.8.0_91\jre\lib\management-agent.jar;
         * D:\Environment\java\jdk1.8.0_91\jre\lib\plugin.jar;
         * D:\Environment\java\jdk1.8.0_91\jre\lib\resources.jar;
         * D:\Environment\java\jdk1.8.0_91\jre\lib\rt.jar;
         * E:\StudyProject\annotation_reflection\out\production\annotation_reflection;
         * D:\WorkingSoftware\IntelliJ IDEA 2020.3.1\lib\idea_rt.jar
         */
    }
}

```

## 创建运行时类的对象

## 获取运行类的完整结构

![image-20210216204339529](.\images\22.png)

### 方法:

> Class c1 = Class.forName("cn.doris.reflection.User"); //获取当前对象的Class
>
> //获得类的名字
>
> c1.getName();// 获得包名 + 类名
>
> c1.getSimpleName();// 获得类名
>
> //获得类的属性
>
> c1.getFields();//只能找到public属性
>
> c1.getDeclaredFields();//找到全部的属性
>
> c1.getDeclaredField("name"); //获得指定属性的值
>
> //获得类的方法
>
> c1.getMethods(); //获得本类及父类的全部public方法
>
> c1.getDeclaredMethods(); //获得本类的所有方法
>
> c1.getMethod("getName", null);//获得指定的方法
>
> //获得类的构造器
>
> c1.getConstructors();
>
> c1.getDeclaredConstructors();
>
> c1.getDeclaredConstructor(String.class, int.class, int.class);//获得指定的构造器

```java
//获取类的信息
public class Demo10_ClassInfo {
    public static void main(String[] args) throws ClassNotFoundException, NoSuchFieldException, NoSuchMethodException {
        Class c1 = Class.forName("cn.doris.reflection.User");
        User user = new User();
        c1 = user.getClass();

        //获得类的名字
        System.out.println(c1.getName());// 获得包名 + 类名
        System.out.println(c1.getSimpleName());// 获得类名

        System.out.println("=======================");

        //获得类的属性
        Field[] fields = c1.getFields();//只能找到public属性
        for (Field field : fields) {
            System.out.println("getFields:" + field);
        }
        fields = c1.getDeclaredFields();//找到全部的属性
        for (Field field : fields) {
            System.out.println("getDeclaredFields:" + field);
        }
        //获得指定属性的值
        Field name = c1.getDeclaredField("name");
        System.out.println(name);

        System.out.println("=======================");

        //获得类的方法
        Method[] methods = c1.getMethods(); //获得本类及父类的全部public方法
        for (Method method : methods) {
            System.out.println("getMethods:" + method);
        }
        methods = c1.getDeclaredMethods(); //获得本类的所有方法
        for (Method method : methods) {
            System.out.println("getDeclaredMethods:" + method);
        }
        System.out.println("=======================");
        //获得指定的方法
        //重载
        Method getName = c1.getMethod("getName", null);
        Method setName = c1.getMethod("setName", String.class);
        System.out.println(getName);
        System.out.println(setName);
        //获得类的构造器
        System.out.println("=======================");
        Constructor[] constructors = c1.getConstructors();
        for (Constructor constructor : constructors) {
            System.out.println("getConstructors:" + constructor);
        }
        constructors = c1.getDeclaredConstructors();
        for (Constructor constructor : constructors) {
            System.out.println("getDeclaredConstructors:" + constructor);
        }
        //获得指定的构造器
        Constructor declaredConstructor = c1.getDeclaredConstructor(String.class, int.class, int.class);
        System.out.println("指定构造器" + declaredConstructor);
    }
}

```

![image-20210217122356362](.\images\23.png)

## 调用运行时类的指定结构

### 有Class对象,能做什么

![image-20210217124548374](.\images\24.png)

### 方法

![image-20210219095443008](.\images\25.png)

![image-20210219095529656](.\images\26.png)

![image-20210219095603902](.\images\27.png)

>//获得Class对象
>
>Class c1 = Class.forName("cn.doris.reflection.User");
>
>//本质上调用了类的无参构造器
>
>User user = (User) c1.newInstance();
>
>//构造器创建对象
>
>Constructor constructor=c1.getDeclaredConstructor(String.class, int.class, int.class);
>   User user1 = (User) constructor.newInstance("长歌",001,17);
>
>//invoke:激活
>// (对象,"方法值")
>setName.invoke(user2, "doris");       
>
>//设置安全检测
>name.setAccessible(true);

```java
//动态的创建对象,通过反射
public class Demo11_DynamicCreateObject {
    public static void main(String[] args) throws ClassNotFoundException, IllegalAccessException, InstantiationException, NoSuchMethodException, InvocationTargetException, NoSuchFieldException {
        //获得Class对象
        Class c1 = Class.forName("cn.doris.reflection.User");

        //构造一个对象
        /*User user = (User) c1.newInstance();//本质上调用了类的无参构造器
        System.out.println(user);*/

        //通过构造器创建对象
        /*Constructor constructor = c1.getDeclaredConstructor(String.class, int.class, int.class);
        User user1 = (User) constructor.newInstance("长歌",001,17);
        System.out.println(user1);*/

        //通过反射调用普通方法
        User user2 = (User) c1.newInstance();
        //通过反射获取一个方法
        Method setName = c1.getDeclaredMethod("setName", String.class);
        //invoke:激活
        // (对象,"方法值")
        setName.invoke(user2, "doris");
        System.out.println(user2.getName());

        //通过反射操作属性
        User user3 = (User) c1.newInstance();
        Field name = c1.getDeclaredField("name");

        //不能直接操作私有属性,我们需要关闭程序的安全检测,属性或方法的setAccessible(true)
        //设置安全检测
        name.setAccessible(true);

        name.set(user3, "doris2");
        System.out.println(user3.getName());
    }
}
```

### 性能检测:

```java
//分析性能问题
public class Demo12_Performance {
    //普通方式调用
    public static void test01() {
        User user = new User();
        long startTime = System.currentTimeMillis();

        for (int i = 0; i < 1000000000; i++) {
            user.getName();
        }

        long endTime = System.currentTimeMillis();
        System.out.println("普通方式执行10亿次:" + (endTime - startTime) + "ms");
    }

    //反射方式调用
    public static void test02() throws NoSuchMethodException, InvocationTargetException, IllegalAccessException {
        User user = new User();
        Class c1 = user.getClass();
        Method getName = c1.getDeclaredMethod("getName", null);
        long startTime = System.currentTimeMillis();

        for (int i = 0; i < 1000000000; i++) {
            getName.invoke(user,null);
        }

        long endTime = System.currentTimeMillis();
        System.out.println("反射方式执行10亿次:" + (endTime - startTime) + "ms");
    }

    //反射方式调用,关闭检测
    public static void test03() throws NoSuchMethodException, InvocationTargetException, IllegalAccessException {
        User user = new User();
        Class c1 = user.getClass();
        Method getName = c1.getDeclaredMethod("getName", null);
        getName.setAccessible(true);
        long startTime = System.currentTimeMillis();

        for (int i = 0; i < 1000000000; i++) {
            getName.invoke(user,null);
        }

        long endTime = System.currentTimeMillis();
        System.out.println("反射方式执行10亿次,关闭检测:" + (endTime - startTime) + "ms");
   }

    public static void main(String[] args) throws NoSuchMethodException, IllegalAccessException, InvocationTargetException {
        test01();
        test02();
        test03();
    }
}
```

##反射操作泛型

![image-20210219111655554](.\images\28.png)

```java
//通过反射获取泛型
public class Demo13_Generic {
    public void test01(Map<String, User> map, List<User>list) {
        System.out.println("test01");
    }

    public Map<String, User> test02() {
        System.out.println("test02");
        return null;
    }

    public static void main(String[] args) throws NoSuchMethodException {
        //根据反射获取方法
        Method method = Demo13_Generic.class.getMethod("test01", Map.class, List.class);
        //获取方法的参数
        Type[] genericExceptionTypes = method.getGenericParameterTypes();
        for (Type genericExceptionType : genericExceptionTypes) {
            //输出
            System.out.println("#" + genericExceptionType);
            //判断参数是否是参数化类型
            if (genericExceptionType instanceof ParameterizedType){
                //强转后获取参数化类型
                Type[] actualTypeArguments = ((ParameterizedType) genericExceptionType).getActualTypeArguments();
                for (Type actualTypeArgument : actualTypeArguments) {
                    System.out.println(actualTypeArgument);
                }
            }
        }

        System.out.println("====================================");
        Method method2 = Demo13_Generic.class.getMethod("test02",null);
        Type genericReturnType = method2.getGenericReturnType();
        if (genericReturnType instanceof ParameterizedType){
            Type[] actualTypeArguments = ((ParameterizedType) genericReturnType).getActualTypeArguments();
            for (Type actualTypeArgument : actualTypeArguments) {
                System.out.println(actualTypeArgument);
            }
        }

    }
}
```

## 反射操作注解

![image-20210219114219419](.\images\29.png)

![image-20210219114249940](.\images\30.png)

```java
//练习反射操作注解
public class Demo14_ORM {
    public static void main(String[] args) throws ClassNotFoundException, NoSuchFieldException {
        Class c1 = Class.forName("cn.doris.reflection.Student2");
        //通过反射获取注解
        Annotation[] annotations = c1.getAnnotations();
        for (Annotation annotation : annotations) {
            System.out.println(annotation);
        }

        //获得注解value
        TableDoris tableDoris = (TableDoris) c1.getAnnotation(TableDoris.class);
        String value = tableDoris.value();
        System.out.println(value);

        //获得类指定的注解
        Field name = c1.getDeclaredField("name");
        FiledDoris annotation = name.getAnnotation(FiledDoris.class);
        System.out.println(annotation.columnName());
        System.out.println(annotation.type());
        System.out.println(annotation.length());
    }
}

@TableDoris("db_student")
class Student2 {
    @FiledDoris(columnName = "db_id", type = "int", length = 10)
    private int id;
    @FiledDoris(columnName = "db_age", type = "int", length = 3)
    private int age;
    @FiledDoris(columnName = "db_name", type = "varchar", length = 200)
    private String name;

    public Student2() {
    }

    public Student2(int id, int age, String name) {
        this.id = id;
        this.age = age;
        this.name = name;
    }

    @Override
    public String toString() {
        return "Student2{" +
                "id=" + id +
                ", age=" + age +
                ", name='" + name + '\'' +
                '}';
    }

    public int getId() {
        return id;
    }

    public void setId(int id) {
        this.id = id;
    }

    public int getAge() {
        return age;
    }

    public void setAge(int age) {
        this.age = age;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }
}

//类名注解
@Target(ElementType.TYPE)
@Retention(RetentionPolicy.RUNTIME)
@interface TableDoris {
    String value();
}

//属性注解
@Target(ElementType.FIELD)
@Retention(RetentionPolicy.RUNTIME)
@interface FiledDoris {
    String columnName();

    String type();

    int length();
}
```

# 泛型

## 泛型知识点

JDK5之后的特性，可以在编译阶段约束操作的数据类型，只支持引用数据类型

泛型的格式：`<数据类型>`

```java
ArrayList<String> list = new ArrayList<>();
```

泛型的好处：

- 统一数据类型
- 把运行时期的问题提前到了编译时期，避免了强制类型转换可能出现的异常，因为在编译阶段类型就能确定下来


泛型的细节：

- Java的泛型是伪泛型，存在泛型的擦除：在编译的时候检查泛型的类型
- 制定泛型的具体类型后，在传递数据时，可以传入该类型或者其子类
- 如果不写泛型，默认Object

## 泛型类

使用场景：当一个类中，某个变量的数据类型不确定时，就可以定义带有泛型的类

```java
// 修饰符 class 类名<类型>{}
public class ArrayList<E>{}
```

E可以理解为变量，不是用来记录数据，而是记录数据的类型，可以写成T、E、K、V

## 泛型方法

方法中形参类型不确定时：

- 使用类名后面定义的泛型
  - 所有方法都能用
- 在方法申明上定义自己的方法
  - 只有本方法能用

```java
// 修饰符 <类型> 返回值类型 方法名(类型 变量名){} 
public <T> void show(T t){}
```

```java

public class ListUtil {
    // 工具类，用来添加多个集合的元素

    //私有化构造方法
    private ListUtil(){}

    public static<E> void addAll1(ArrayList<E> list, E e1, E e2, E e3, E e4){
        list.add(e1);
        list.add(e2);
        list.add(e3);
        list.add(e4);
    }

    public static<E> void addAll2(ArrayList<E> list, E...e){
        for (E ele : e) {
            list.add(ele);
        }
    }

}
```

#  泛型接口

格式：

```java
// 修饰符 interface 接口名<类型>{}
public inteface List<E>{}
```

使用方法：

1. 实现类给出具体类型
2. 实现类延续泛型，创建对象时再确定

```java
public class GenericsDemo2 {
    public static void main(String[] args) {
        MyArrayList1 list1 = new MyArrayList1();
        list1.add("aaa");
        list1.add("aaa");
        list1.add("aaa");

        MyArrayList2<String> list2 = new MyArrayList2<>();
        list2.add("aaa");
        list2.add("aaa");
        list2.add("aaa");
    }
}

```

## 泛型的继承和通配符

泛型不具备继承性，但是数据具备继承性

```java
public class GenericsDemo3 {
    public static void main(String[] args) {
        ArrayList<Ye> list1 = new ArrayList<>();
        ArrayList<Fu> list2 = new ArrayList<>();
        ArrayList<Zi> list3 = new ArrayList<>();

        // 调用method方法
        method(list1);
        // 下方报错（泛型不具备继承性）
        // method(list2);
        // method(list3);

        // 数据具备继承性
        list1.add(new Ye());
        list1.add(new Fu());
        list1.add(new Zi());

        // 通配符
        method2(list1);
        method2(list2);
        method2(list3);

        method3(list1);
        method3(list2);
        method3(list3);
    }

    /*
    * 这里的泛型里面写的是什么类型，那就只能传递什么类型的数据
    * */
    public static void method(ArrayList<Ye> list){}

    public static void method2(ArrayList<? extends Ye> list){}

    public static void method3(ArrayList<? super Zi> list){}
}


class Ye{}

class Fu extends Ye{}

class Zi extends Fu{}
```



当不确定方法中传入的数据类型时，可以使用泛型，但泛型可以接受任意的数据类型，无法做出类型的限制

泛型的通配符：

- `?`: 可以表示不确定的类型，也可以进行类型的限定
- `? extends E`: 表示可以传递E或者E所有的子类类型
- `? super E`: 表示可以传递E或者E所有的父类类型

应用场景

- 如果在定义类、方法、接口的时候：如果类型不确定，可以使用泛型
- 如果类型不确定，但知道以后只能传递某个继承体系中的类型，可以使用通配符
  - 关键点：通配符可以限定类型的范围