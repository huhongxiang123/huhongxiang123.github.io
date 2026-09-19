import re

#正则的使用方法

rule = r'苹果'
text = '苹果很好吃，香蕉也很好吃，火龙果也好吃，但我最爱苹果'
#找到text中的所有的苹果
result = re.findall(rule,text)
print(result)

rule = r'".."'  #.就代表一个字符
text = '"苹果"很好吃，"香蕉"也很好吃，"火龙果"也好吃，但我最爱"苹果"'
#找到text中的所有的苹果
result = re.findall(rule,text)
print(result)

rule = r'".+?"'  #.就代表一个字符  +?代表内容出现了很多次，但我也不知道多少次，你就把引号内容提取给我就行了
text = '"苹果"很好吃，"香蕉"也很好吃，"火龙果"也好吃，但我最爱"苹果","香蕉你个banana"'
#找到text中的所有的苹果
result = re.findall(rule,text)
print(result)

rule = r'"(.+?)"'  #.就代表一个字符  +?代表内容出现了很多次，但我也不知道多少次，你就把引号内容提取给我就行了
text = '"苹果"很好吃，"香蕉"也很好吃，"火龙果"也好吃，但我最爱"苹果","香蕉你个banana"'
#找到text中的所有的苹果
result = re.findall(rule,text)
print(result)
