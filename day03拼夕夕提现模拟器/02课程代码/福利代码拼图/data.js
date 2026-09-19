(function (global) {
  "use strict";

  var categories = [
    { key: "io", label: "输入输出", description: "print 与 input 基础" },
    { key: "variables", label: "变量计算", description: "赋值与四则运算" },
    { key: "condition", label: "判断练习", description: "if / else 结构" },
    { key: "loop", label: "循环练习", description: "for / while 入门" }
  ];

  var puzzles = [
    {
      id: 1,
      category: "io",
      title: "输入姓名并输出",
      description: "请将代码恢复成正确顺序，使程序先获取姓名，再输出问候和姓名。",
      correctOrder: [
        'name = input("请输入姓名：")',
        'print("你好")',
        'print(name)'
      ],
      explanation: "代码先读取用户输入，再输出固定问候语，最后打印用户的姓名。"
    },
    {
      id: 2,
      category: "io",
      title: "输入年龄",
      description: "调整顺序，让程序先读入年龄，再输出提示和年龄值。",
      correctOrder: [
        'age = input("请输入年龄：")',
        'print("你输入的年龄是")',
        'print(age)'
      ],
      explanation: "先保存输入值，再按顺序输出说明文字和变量内容。"
    },
    {
      id: 3,
      category: "io",
      title: "双输入展示",
      description: "先输入城市和喜欢的食物，然后按顺序输出。",
      correctOrder: [
        'city = input("你在哪个城市？")',
        'food = input("你喜欢什么食物？")',
        'print("你在")',
        'print(city)',
        'print(food)'
      ],
      explanation: "两个 input 都需要放在输出之前，否则变量还没有值。"
    },
    {
      id: 4,
      category: "io",
      title: "分数读取",
      description: "程序应该先读取分数并转成整数，再输出结果。",
      correctOrder: [
        'score = int(input("请输入分数："))',
        'print("你的分数是")',
        'print(score)'
      ],
      explanation: "int(input()) 用于先输入再转换，顺序不能反。"
    },
    {
      id: 5,
      category: "io",
      title: "欢迎信息",
      description: "让欢迎语、输入用户名和结果输出形成正确流程。",
      correctOrder: [
        'print("欢迎来到 PyPuzzle")',
        'username = input("请输入用户名：")',
        'print("当前用户：")',
        'print(username)'
      ],
      explanation: "通常先展示提示，再读取输入，最后输出输入结果。"
    },
    {
      id: 6,
      category: "variables",
      title: "两数求和",
      description: "把变量赋值、计算和输出按执行顺序排列。",
      correctOrder: [
        'a = 3',
        'b = 5',
        'c = a + b',
        'print(c)'
      ],
      explanation: "先定义变量 a、b，再用它们计算 c，最后输出。"
    },
    {
      id: 7,
      category: "variables",
      title: "计算总价",
      description: "让程序先定义单价和数量，再算总价并打印。",
      correctOrder: [
        'price = 12',
        'count = 4',
        'total = price * count',
        'print(total)'
      ],
      explanation: "变量计算依赖前面的赋值，所以赋值必须在前。"
    },
    {
      id: 8,
      category: "variables",
      title: "减法和除法",
      description: "请按顺序完成变量赋值后，再进行两次输出。",
      correctOrder: [
        'x = 10',
        'y = 2',
        'print(x - y)',
        'print(x / y)'
      ],
      explanation: "变量 x、y 必须先存在，后面的表达式才能执行。"
    },
    {
      id: 9,
      category: "variables",
      title: "字符串变量",
      description: "先定义两个字符串变量，再依次输出。",
      correctOrder: [
        'name = "Python"',
        'level = "入门"',
        'print(name)',
        'print(level)'
      ],
      explanation: "字符串变量和数字变量一样，先赋值后使用。"
    },
    {
      id: 10,
      category: "variables",
      title: "圆面积",
      description: "请恢复计算圆面积的代码顺序。",
      correctOrder: [
        'radius = 5',
        'area = 3.14 * radius * radius',
        'print("面积为")',
        'print(area)'
      ],
      explanation: "先有半径，再算面积，最后输出文字和结果。"
    },
    {
      id: 11,
      category: "condition",
      title: "及格判断",
      description: "把 if / else 结构恢复正确，并保持缩进关系。",
      correctOrder: [
        'score = 85',
        'if score >= 60:',
        '    print("及格")',
        'else:',
        '    print("不及格")'
      ],
      explanation: "if 和 else 是一组分支，分支里的 print 需要缩进。"
    },
    {
      id: 12,
      category: "condition",
      title: "成年判断",
      description: "程序应先定义年龄，再判断并输出结果。",
      correctOrder: [
        'age = 16',
        'if age >= 18:',
        '    print("可以投票")',
        'else:',
        '    print("未成年")'
      ],
      explanation: "先有 age 的值，条件判断才有意义。"
    },
    {
      id: 13,
      category: "condition",
      title: "奇偶判断",
      description: "恢复 if / else 语句，让程序判断一个数是奇数还是偶数。",
      correctOrder: [
        'num = 7',
        'if num % 2 == 0:',
        '    print("偶数")',
        'else:',
        '    print("奇数")'
      ],
      explanation: "num % 2 == 0 表示可以被 2 整除，即偶数。"
    },
    {
      id: 14,
      category: "condition",
      title: "天气选择",
      description: "根据 weather 的值执行不同分支，保持顺序和缩进。",
      correctOrder: [
        'weather = "sunny"',
        'if weather == "sunny":',
        '    print("去散步")',
        'else:',
        '    print("在家看书")'
      ],
      explanation: "先定义 weather，再进入 if 判断并执行对应分支。"
    },
    {
      id: 15,
      category: "condition",
      title: "密码校验",
      description: "恢复输入密码并判断结果的代码顺序。",
      correctOrder: [
        'password = input("请输入密码：")',
        'if password == "123456":',
        '    print("登录成功")',
        'else:',
        '    print("密码错误")'
      ],
      explanation: "先获取 password，再比较并输出登录结果。"
    },
    {
      id: 16,
      category: "loop",
      title: "for 循环输出",
      description: "请恢复 for 循环，让程序输出 0 到 2。",
      correctOrder: [
        'for i in range(3):',
        '    print(i)'
      ],
      explanation: "range(3) 产生 0、1、2，循环体 print(i) 需要缩进。"
    },
    {
      id: 17,
      category: "loop",
      title: "循环求和",
      description: "让 total 从 0 开始，循环累加 1 到 3，并输出结果。",
      correctOrder: [
        'total = 0',
        'for i in range(1, 4):',
        '    total = total + i',
        'print(total)'
      ],
      explanation: "先初始化 total，循环内累加，循环结束后再输出。"
    },
    {
      id: 18,
      category: "loop",
      title: "while 基础",
      description: "恢复 while 循环，让程序依次输出 1 到 3。",
      correctOrder: [
        'n = 1',
        'while n <= 3:',
        '    print(n)',
        '    n = n + 1'
      ],
      explanation: "while 循环每次输出后都要更新 n，否则会死循环。"
    },
    {
      id: 19,
      category: "loop",
      title: "遍历字符串",
      description: "通过 for 循环依次输出字符串中的字符。",
      correctOrder: [
        'for ch in "abc":',
        '    print(ch)'
      ],
      explanation: "for 会按顺序遍历字符串中的每个字符。"
    },
    {
      id: 20,
      category: "loop",
      title: "循环中的判断",
      description: "恢复 for + if 的基础结构，只输出偶数。",
      correctOrder: [
        'for i in range(5):',
        '    if i % 2 == 0:',
        '        print(i)'
      ],
      explanation: "先循环 i，再在循环体内部判断是否为偶数并输出。"
    }
  ];

  global.PyPuzzleData = {
    categories: categories,
    puzzles: puzzles,
    version: "1.0.0"
  };
})(window);
