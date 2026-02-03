# xpath 是一门语言：在 xml文档中搜索内容的一门语言
# html是xml的一个子集，所以可以在 html 上使用 xpath。
# 先安装：pip install -i https://pypi.tuna.tsinghua.edu.cn/simple/ lxml  -->已

# xpath路径 可以在网页源代码 copy xpath，但是记得copy对，有些是hidden标签

from lxml import etree

# 你的XML字符串，
xml = '''
<book>
<id>1</id>
<name>野花遍地香</name>
<price>1.23</price>
<nick>臭豆腐</nick>
<author>
    <nick id="10086">周大强</nick>
    <nick id="10010">周芷若</nick>
    <nick class="joy">周杰伦</nick>
    <nick class="jolin">蔡依林</nick>
    <div>
    <nick>惹了</nick>
    </div>
</author>
</book>
'''



# 解析XML字符串为ElementTree对象
tree = etree.XML(xml)

# eg.
# html = etree.HTML(resp.text)
# divs = html.xpath("......")
# for div in divs:
#     price = div.xpath(".//div[@class='price']")[0]
#     title = "saas".join(div.xpath("./div/div/a[2]/text()"))

# 用XPath查询：

result1 = tree.xpath("/book") #/表示层级关系，第一个/是根节点,print只打印该book元素所在编号
# 获取所有nick标签的文本
all_nicks = tree.xpath('//nick/text()')# //是后代的意思
print(all_nicks)  # 输出：['臭豆腐', '周大强', '周芷若', '周杰伦', '蔡依林', '惹了']

# 如果路径之间有 * 号则是通配符，还有“ . ”是在该路径内包裹的东西中继续查找
# 获取id为10086的nick文本
specific_nick = tree.xpath('//nick[@id="10086"]/text()')
print(specific_nick)  # 输出：['周大强']