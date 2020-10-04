## 开发环境为 Python 3.6.2
#TODO  生成静态界面：

import tkinter as tk
from tkinter import ttk
import parser

# import functions as fs ## fail

class TkGUI(tk.Tk):
    FONT_LARGE = ("Calibri", 12)  	# selects the font of the text inside buttons
    FONT_MED = ("Calibri", 10)

    # Max rows and columns in the GUI
    # 这个row和column 不包括 display 和 底部的等于符号
    MAX_ROW = 4 
    MAX_COLUMN = 5

    NEW_OPERATION = False

    # defining private variables:
    # ans 表示保留的上一步的结果；最后的视图是在等于符号那一行
    ans = 0

    # memory 表示保留的与记忆功能相关的一个值
    memory = 0 

    # index 表示插入字符所在的位置指针
    index = 0

    #* 定义 display是TkGUI的一个属性，表示的就是那个最主要的 entry
    display = None #声明之后再初始化。



    #* 在 class 这个抽象层上面的初始化
    def __init__(self):
        
        #! self 作为是一个参数，是针对一般的函数，例如写在fs里面的函数
        super(TkGUI, self).__init__()

        self.title("Python GUI Calculator")
        self.resizable(width=False, height=False)

        # Configure default theme
        style = ttk.Style(self)
        style.theme_use('clam')


        #* 下面两步做的是统一配置格子，但是最后一行的格子与之前的不一样，所以不能统一配置
        for row in range(self.MAX_ROW):
            self.columnconfigure(row, pad=3) # pad参数设定格子之间的间距

        for column in range(self.MAX_COLUMN-1):
            self.rowconfigure(column, pad=3)

        #* display 这个属性初始化，动态混入，所以不需要声明。
        self.display = tk.Entry(self, font=("Calibri", 13))
        self.display.grid(row=1, columnspan=6, sticky=tk.W + tk.E)  # 最上面是row=1


        self._init_gui()




    #* 在 gui 这个层次上面的初始化：
    def _init_gui(self):   
        #think: self parameter 虽然是缺省的，但是在函数体内部显式调用需要标识self，否则就是invalid id 
        
        ##TODO .STATIC

        #think:
        '''
        对于button的command命令，什么时候使用lambda，什么时候加括号
        传参使用lambda；
        其他时候都调用过程就可以了；


        '''


        #* one to zero ,these 10 numbers here:
        one = tk.Button(
            self, text="1", command=lambda: self.get_variables(1), font=self.FONT_LARGE)
        one.grid(row=2, column=0) #column 是从0开始的

        two = tk.Button(
            self, text="2", command=lambda: self.get_variables(2), font=self.FONT_LARGE)
        two.grid(row=2, column=1)

        three = tk.Button(
            self, text="3", command=lambda: self.get_variables(3), font=self.FONT_LARGE)
        three.grid(row=2, column=2)

        four = tk.Button(
            self, text="4", command=lambda: self.get_variables(4), font=self.FONT_LARGE)
        four.grid(row=3, column=0)

        five = tk.Button(
            self, text="5", command=lambda: self.get_variables(5), font=self.FONT_LARGE)
        five.grid(row=3, column=1)

        six = tk.Button(
            self, text="6", command=lambda: self.get_variables(6), font=self.FONT_LARGE)
        six.grid(row=3, column=2)

        seven = tk.Button(
            self, text="7", command=lambda: self.get_variables(7), font=self.FONT_LARGE)
        seven.grid(row=4, column=0)

        eight = tk.Button(
            self, text="8", command=lambda: self.get_variables(8), font=self.FONT_LARGE)
        eight.grid(row=4, column=1)

        nine = tk.Button(
            self, text="9", command=lambda: self.get_variables(9), font=self.FONT_LARGE)
        nine.grid(row=4, column=2)

        zero = tk.Button(
            self, text="0", command=lambda: self.get_variables(0), font=self.FONT_LARGE)
        zero.grid(row=5, column=0)

    
        #* 生成小数点按钮 dot button；考虑到Python是动态类型，我们get_variables('.'),这样做也没错。。
        dot = tk.Button(
            self, text=". ", command=lambda: self.get_variables('.'), font=self.FONT_LARGE)
        dot.grid(row=5, column=1)


        #* 生成清除按钮 clear button：
        clear = tk.Button(self, text="C", command=self.clear_all,
                        font=self.FONT_LARGE, foreground="red")
        clear.grid(row=5, column=2)


        #* 生成ANS按钮，可以获得ans的值：
        ans = tk.Button(self, text="ANS", command=self.insert_ans, font=self.FONT_LARGE)
        ans.grid(row=6,column=0)


        #* 生成结果按钮，也就是底部的等于符号
        result = tk.Button(self, text="=", command=self.calculate,
                           font=self.FONT_LARGE, foreground="red")
        result.grid(row=6,column=4)

        #* 生成记忆相关的按钮
        # mr: memory return
        mr_b = tk.Button(self, text="MR", command=self.mr, font=self.FONT_LARGE)
        mr_b.grid(row=2, column=4)

        # mc: memory clear
        mc_b = tk.Button(self, text="MC", command=self.mc, font=self.FONT_LARGE)
        mc_b.grid(row=3, column=4)

        # m-: memory devide:  memory-=ans
        md_b = tk.Button(self, text="M- ", command=self.md, font=self.FONT_LARGE)
        md_b.grid(row=4, column=4)

        # m+: memory plus:  memory+=ans
        mp_b = tk.Button(self, text="M+", command=self.mp, font=self.FONT_LARGE)
        mp_b.grid(row=5,column=4)


        #* Adding Features:
        
        # 撤销操作：
        undo_b = tk.Button(self, text="<-", command=self.undo, font=self.FONT_LARGE, foreground="red")
        undo_b.grid(row=6,column=2)


        #* 定义操作符：
        plus = tk.Button(
            self, text="+", command=lambda: self.get_operation("+"), font=self.FONT_LARGE)
        plus.grid(row=2, column=3)

        minus = tk.Button(
            self, text="-", command=lambda: self.get_operation("-"), font=self.FONT_LARGE)
        minus.grid(row=3, column=3)

        multiply = tk.Button(
            self, text="*", command=lambda: self.get_operation("*"), font=self.FONT_LARGE)
        multiply.grid(row=4, column=3)

        divide = tk.Button(
            self, text="/", command=lambda: self.get_operation("/"), font=self.FONT_LARGE)
        divide.grid(row=5, column=3)




    #TODO .DYNAMIC 放弃了，还是写成一个类的方法算了。

    def get_variables(self, num):
        """
        Gets the user input for operands and puts it inside the entry widget.
        If a new operation is being carried out, then the display is cleared.

        提升UE的一个设计就是，在键入数字的时候判断前一位是否为运算符：
            如果是，那么清零；
            如果不是，就继续追加；

        
        """
        if self.NEW_OPERATION:  #可见new_operation是判断是否清零的标准。
            self.clear_all(new_operation=False)
        self.display.insert(self.index, num)
        self.index += 1

            
    def get_operation(self, operator):
        """Gets the operand the user wants to apply on the functions."""
        self.display.insert(self.index, operator)
        self.index += len(operator)
        #test -- ok 
        self.NEW_OPERATION = False
        


    ##* 以上两个函数是函数，需要lambda来传参
    ##* 下面的函数就都是过程了。

    def clear_all(self, new_operation=True):
        """clears all the content in the Entry widget."""
        self.display.delete(0, tk.END)
        #? 需要将index复位吗？ i think not so 
        # self.index = 0
        self.NEW_OPERATION = new_operation


    def insert_ans(self, new_operation=False):
        self.display.insert(self.index, self.ans)
        # self.index += len(self.ans)
        #! ans is-a int , has no length
        ans_s = str(self.ans)
        self.index += len(ans_s)
        
    def undo(self):
        # 撤销上一步操作，本质就是将 display的末尾字符删除掉；无可否认的一点就是，处理速度确实慢的。
        whole_string = self.display.get()
        if len(whole_string):        
            new_string = whole_string[:-1]
            self.clear_all(new_operation=False)
            self.display.insert(0, new_string)
        else:
            self.clear_all() 
            self.display.insert(0, "Error, press AC")

        


    #? new_operation 是干什么的？
    #A 描述是否为新的一个表达式。

    # memory return
    def mr(self):
        self.display.insert(self.index, self.memory)

    # memory clear
    def mc(self):
        self.memory = 0


    # m-: memory devide:  memory-=ans
    #Bug：按照题目的意思，应该是显示值的处理，而不是ans的处理，所以要改成部分与calculate函数相似的形式。
    def md(self):
        whole_string = self.display.get()
        
        #检查 display内容是否为纯数字：
        numbers_ls = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.', '-']
        for i in whole_string:
            if i not in numbers_ls:
                self.clear_all()
                self.display.insert(0, "Error!")
        
        self.memory -= eval(whole_string)
        

    # m+: memory plus:  memory+=ans    
    def mp(self):
        whole_string = self.display.get()
        
        #检查 display内容是否为纯数字：
        numbers_ls = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.', '-']
        
        for i in whole_string:
            if i not in numbers_ls:
                self.clear_all()
                self.display.insert(0, "Error!")
        
        self.memory += eval(whole_string)
        


    def calculate(self):
        '''
            the eval is evil !!!
        一个eval函数解决了所有的问题;
        但是，安全性问题很重要！所以我们使用 parser 这个模块来解析参数是否可能污染程序。

        但是，还是有一个“巧妙的Bug”，在display里面键入 ** 符号，会使用指数进行计算。

        '''

        whole_string = self.display.get()
        try:
            formulae = parser.expr(whole_string).compile()
            result = eval(formulae)
            self.ans = result # 保留ans
            self.clear_all()
            self.display.insert(0, result)
            self.index = len(str(result))
            
        except Exception:
            self.clear_all()
            self.display.insert(0, "Error!")






        #TODO # adding new operations,but this part maybe less important
        # multi_pi = tk.Button(self, text="pi", command=lambda: self.get_operation(
        #     "*3.14"), font=self.FONT_LARGE)
        # multi_pi.grid(row=2, column=4)

        # modulo = tk.Button(
        #     self, text="%", command=lambda:  self.get_operation("%"), font=self.FONT_LARGE)
        # modulo.grid(row=3, column=4)

        # left_bracket = tk.Button(
        #     self, text="(", command=lambda: self.get_operation("("), font=self.FONT_LARGE)
        # left_bracket.grid(row=4, column=4)

        # right_bracket = tk.Button(
        #     self, text=")", command=lambda: self.get_operation(")"), font=self.FONT_LARGE)
        # right_bracket.grid(row=4, column=5)        

        # exp = tk.Button(self, text="exp",
        #                 command=lambda: self.get_operation("**"), font=self.FONT_MED)
        # exp.grid(row=5, column=4)

        # factor = tk.Button(
        #     self, text="x!", command=lambda: self.factorial("!"), font=self.FONT_LARGE)
        # factor.grid(row=3, column=5)

        # square = tk.Button(
        #     self, text="^2", command=lambda: self.get_operation("**2"), font=self.FONT_MED)
        # square.grid(row=5, column=5)

        # To be added :
        # sin, cos, log, ln
        # these may use the para operation_length.


        
    #* def undo(self):
    #     pass

    def run(self):
            #* Initiate event loop.
            self.mainloop()


