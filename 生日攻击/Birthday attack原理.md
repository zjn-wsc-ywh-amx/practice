# Birthday attack原理

这个问题在数学上早有原型，叫做"[生日问题](https://en.wikipedia.org/wiki/Birthday_problem)"（birthday problem）：一个班级需要有多少人，才能保证每个同学的生日都不一样？

答案很出人意料。如果至少两个同学生日相同的概率不超过5%，那么这个班只能有7个人。事实上，一个23人的班级有50%的概率，至少两个同学生日相同；50人班级有97%的概率，70人的班级则是99.9%的概率（计算方法见后文）。

这意味着，如果哈希值的取值空间是365，只要计算23个哈希值，就有50%的可能产生碰撞。也就是说，哈希碰撞的可能性，远比想象的高。实际上，有一个近似的公式。

![img](https://www.wangbase.com/blogimg/asset/201809/bg2018090509.png)

上面公式可以算出，50% 的哈希碰撞概率所需要的计算次数，N 表示哈希的取值空间。生日问题的 N 就是365，算出来是 23.9。这个公式告诉我们，哈希碰撞所需耗费的计算次数，跟取值空间的平方根是一个数量级。

这种利用哈希空间不足够大，而制造碰撞的攻击方法，就被称为生日攻击（birthday attack）。

## 四、数学推导

这一节给出生日攻击的数学推导。

至少两个人生日相同的概率，可以先算出所有人生日互不相同的概率，再用 1 减去这个概率。

我们把这个问题设想成，每个人排队依次进入一个房间。第一个进入房间的人，与房间里已有的人（0人），生日都不相同的概率是`365/365`；第二个进入房间的人，生日独一无二的概率是`364/365`；第三个人是`363/365`，以此类推。

因此，所有人的生日都不相同的概率，就是下面的公式。

![img](https://www.wangbase.com/blogimg/asset/201809/bg2018090501.png)

上面公式的 n 表示进入房间的人数。可以看出，进入房间的人越多，生日互不相同的概率就越小。

这个公式可以推导成下面的形式。

![img](https://www.wangbase.com/blogimg/asset/201809/bg2018090502.png)

那么，至少有两个人生日相同的概率，就是 1 减去上面的公式。

![img](https://www.wangbase.com/blogimg/asset/201809/bg2018090503.png)

## 五、哈希碰撞的公式

上面的公式，可以进一步推导成一般性的、便于计算的形式。

根据泰勒公式，指数函数 ex 可以用多项式展开。

![img](https://www.wangbase.com/blogimg/asset/201809/bg2018090504.png)

如果 x 是一个极小的值，那么上面的公式近似等于下面的形式。

![img](https://www.wangbase.com/blogimg/asset/201809/bg2018090505.png)

现在把生日问题的`1/365`代入。

![img](https://www.wangbase.com/blogimg/asset/201809/bg2018090506.png)

因此，生日问题的概率公式，变成下面这样。

![img](https://www.wangbase.com/blogimg/asset/201809/bg2018090507.png)

假设 d 为取值空间（生日问题里是 365），就得到了一般化公式。

![img](https://www.wangbase.com/blogimg/asset/201809/bg2018090508.png)

上面就是哈希碰撞概率的公式。





引用 https://blog.csdn.net/u014162133/article/details/82465538?ops_request_misc=%257B%2522request%255Fid%2522%253A%2522165827686516782395327207%2522%252C%2522scm%2522%253A%252220140713.130102334..%2522%257D&request_id=165827686516782395327207&biz_id=0&utm_medium=distribute.pc_search_result.none-task-blog-2~all~sobaiduend~default-1-82465538-null-null.142^v32^pc_rank_34,185^v2^control&utm_term=birthday%20attack&spm=1018.2226.3001.4187