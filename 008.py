import pandas as pd
dataset = pd.read_csv("E:\\data\\Market_Basket_Optimisation.csv")
print(dataset.shape)
dataset.head()


# 转换Numpy数组类型
import numpy as np
transaction = []
for i in range(0, dataset.shape[0]):
    for j in range(0, dataset.shape[1]):
        transaction.append(dataset.values[i,j])
transaction = np.array(transaction)
print(transaction)

# 统计并可视化商品购买频次
import pandas as pd
df = pd.DataFrame(transaction, columns=["items"])
df["incident_count"] = 1
indexNames = df[df['items'] == "nan" ].index
df.drop(indexNames , inplace=True)
# 对商品名称进行分组，计算每种商品的购买总次数，取前5序号
df_table = df.groupby("items").sum().sort_values("incident_count", ascending=False).reset_index()
df_table.head(5).style.background_gradient(cmap='Greens')


# 可视化前50个
import plotly.express as px
df_table["all"] = "Top 50 items"
fig = px.treemap(df_table.head(50), path=['all', "items"], values='incident_count',
                  color=df_table["incident_count"].head(50), hover_data=['items'],
                  color_continuous_scale='Greens',
                )
fig.show()



# 将每笔交易转换为单独的列表，并将它们收集到Numpy数组中
transaction = []
for i in range(dataset.shape[0]):
    transaction.append([str(dataset.values[i,j]) for j in range(dataset.shape[1])])
transaction = np.array(transaction)



from mlxtend.preprocessing import TransactionEncoder

# 初始化TransactionEncoder并将数据转换为布尔值
te = TransactionEncoder()
te_ary = te.fit(transaction).transform(transaction)
dataset = pd.DataFrame(te_ary, columns=te.columns_)
dataset.head()



first30 = df_table["items"].head(30).values
dataset = dataset.loc[:,first30]
print(dataset.shape)

# 运行FP-growth算法
from mlxtend.frequent_patterns import fpgrowth
res = fpgrowth(dataset, min_support=0.05, use_colnames=True)
res.head(10)


from mlxtend.frequent_patterns import association_rules
res = association_rules(res, metric="lift", min_threshold=1)
# 根据置信度对值进行排序
res.sort_values("confidence", ascending=False)




