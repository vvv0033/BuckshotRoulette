import sys
import csv
import random
import json
import os

# 获取脚本的绝对路径
script_path = os.path.abspath(__file__)

# 获取脚本所在的目录
script_dir = os.path.dirname(script_path)

# 构建文件路径
data_dir = r'C:\ProgramData\Lunpandu'
data_file_path = os.path.join(data_dir, 'data.csv')
data1_file_path = os.path.join(data_dir, 'data1.csv')
data2_file_path = os.path.join(data_dir, 'data2.csv')

# 确保数据目录存在
os.makedirs(data_dir, exist_ok=True)


def remove_player_by_name(player_name: str, p_list: list) -> bool:
    """通过实例的name属性删除列表中第一个符合条件的实例，返回操作是否成功"""
    # 创建列表的副本
    temp_list = p_list.copy()
    
    # 尝试移除玩家
    for player in temp_list:
        if player.name == player_name:
            p_list.remove(player)
            return True  # 返回True表示成功移除玩家
    return False  # 如果没有找到玩家，返回False

def create(p_list:list):
    """将一个player实例加入选定列表"""
    finish = False
    while not finish:
        name = str(input("choose a name: "))
        if name == "Cheese Sandwich" or any(p.name == name for p in p_list):
            print("This name is used, please try again.")
        else:
            new_player = player(name)
            p_list.append(new_player)
            finish = True

def rearrange_list(num):
    n = num//2
    m = num//2 + num%2
    # 创建一个包含n个True和m个False的列表
    boolean_list = [True] * n + [False] * m
    # 使用random.shuffle方法随机打乱列表
    random.shuffle(boolean_list)
    return boolean_list

class player:
    """管理玩家数据的类"""
    def __init__(self,name,hp=4,tools=[],level=0):
        self.name = name
        self.hp = hp
        self.tools = tools
        self.level = level

    def have_tools(self,num):
        tools_list = ["knife","cigarette","magnifying glass","handcuffs","drink"]
        for i in range(num):
            n = random.randint(0,len(tools_list)-1)
            self.tools.append(tools_list[n])

    def __str__(self):
        tools_str = str(self.tools) if self.tools else "[]"  
        n = "name:{} hp:{} tools:{} level:{}".format(self.name,self.hp,tools_str,self.level)
        return n
    
    def show_hp(self):
        print("The hp of {} is {}".format(self.name,self.hp))

    def to_csv(self):
            # 使用json.dumps将tools列表转换为JSON格式的字符串
            tools_str = json.dumps(self.tools) if self.tools else "[]"
            
            # 返回一个列表，包含所有需要写入CSV的字段
            return [self.name, str(self.hp), tools_str, str(self.level)]

    @classmethod
    def from_csv(cls, row):
        name, hp, tools_str, level = row
        # 使用json.loads将JSON格式的字符串转换回列表
        tools = json.loads(tools_str) if tools_str != "[]" else []
        return cls(name, int(hp), tools, int(level))
    
class gun:
    """管理枪数据的类"""
    def __init__(self):
        self.num = 6
        self.order = []

    def reload(self):
        self.num = random.randint(2,8)
        self.order = rearrange_list(self.num)
        n = sum(1 for value in self.order if value)
        m = sum(1 for value in self.order if not value)
        print("The gun is reloaded, {} real, {} fake.".format(n,m))

    def shoot(self,player,opposite):
        if self.order == []:
            self.reload()
        x = self.order.pop(0)
        if x:
            player.hp -= 1
            print("Ball cartridge!") 
            player.show_hp()
            opposite.show_hp()
            print("")
        if not x:
            print("Blank cartridge\n")
        return x
    
class lunpandu:
    """游戏资源及各行为的类"""
    def __init__(self):
        self.edition = 1.0
        self.maker = "Sihan CHEN"
    
    def __str__(self):
        n = "Edition{}\nMaker{}\nThanks for your playing!".format(self.edition,self.maker)
        return n

    def menu(self):
        """游戏目录"""
        self.save()
        choose = input("\nWelcome (start/manage/rule/about/exit) ")
        if choose == "manage":
            self.manage()
        elif choose == "about":
            print ("Edition：{}\nMaker：{}\nThanks for your playing!".format(self.edition,self.maker))
        elif choose == "start":
            self.run_game()
        elif choose =="rule":
            print("玩家开始游戏后会和恶魔面对面坐着，每回合开始恶魔会在霰弹枪中填装任意数量的实弹和空弹，填装前会为玩家们展示具体有几发，填装后顺序随机，可以选择射击对方或自己。")
            print("之后玩家与恶魔依次出手，可以选择向对方开枪或者向自己开枪。如果向自己开枪并且是空弹，则对方跳过一回合，如果是实弹则减少一点生命。向对方开枪如果是空弹则不造成任何效果，如果是实弹则降低对方一点生命。双方直到一方生命归零，游戏结束。")
        elif choose == "exit":
            sys.exit("Thanks for playing.")
        else:
            print("This input makes no sense.")

    def manage(self):
        """管理玩家"""
        while True:
            operation = input("Choose your operation:(check/delete/create/back): ")
            if operation in ["check", "delete","create","back"]:
                break
            else:
                print("This input makes no sense. Please try again.")

# 现在 choose 包含了一个有效的输入，可以继续后续的操作
        if operation =="check":
            print("\nalive players:")
            for player in player_list:
                print(player)
            print("\ndead players:")
            for player in dead_list:
                print(player)
        elif operation == "delete":
            player_name_to_remove = input("Choose the name of the player that you want to delete.")
            if remove_player_by_name(player_name_to_remove, player_list):
                print(f"玩家 {player_name_to_remove} 已成功移除。")
            else:
                print(f"玩家 {player_name_to_remove} 未找到。")
        elif operation == "create":
            create(player_list)
        self.menu()

    def save(self):
        # 保存玩家数据到CSV文件
        with open(data_file_path, 'w', newline='') as file:
            writer = csv.writer(file)
            for player in player_list:
                writer.writerow(player.to_csv())

        # 保存死亡玩家数据到CSV文件
        with open(data1_file_path, 'w', newline='') as file:
            writer = csv.writer(file)
            for player in dead_list:
                writer.writerow(player.to_csv())

        # 保存电脑玩家数据到CSV文件
        with open(data2_file_path, 'w', newline='') as file:
            writer = csv.writer(file)
            for player in computer_list:
                writer.writerow(player.to_csv())

    def read(self):
        global player_list, dead_list, computer_list
        
        # 初始化玩家列表
        player_list = []
        dead_list = []
        computer_list = []

        try:
            with open(data_file_path, 'r') as file:
                reader = csv.reader(file)
                for row in reader:
                    try:
                        player_list.append(player.from_csv(row))
                    except ValueError as e:
                        print("Skipping invalid row: {}".format(e))
        except FileNotFoundError:
            print("data.csv not found. Starting with an empty player list.")
        
        try:
            with open(data1_file_path, 'r') as file:
                reader = csv.reader(file)
                for row in reader:
                    try:
                        dead_list.append(player.from_csv(row))
                    except ValueError as e:
                        print("Skipping invalid row: {}".format(e))
        except FileNotFoundError:
            print("data1.csv not found. Starting with an empty dead player list.")
        
        try:
            with open(data2_file_path, 'r') as file:
                reader = csv.reader(file)
                for row in reader:
                    try:
                        computer_list.append(player.from_csv(row))
                    except ValueError as e:
                        print("Skipping invalid row: {}".format(e))
        except FileNotFoundError:
            print("data2.csv not found. Starting with an empty computer player list.")

        return player_list, dead_list, computer_list

    def get_shoot_choice(self):
        while True:
            choose3 = input("Who?(I/dealer/back): ")
            if choose3 in ["I", "dealer"]:
                return choose3
            elif choose3 == "back":
                return None
            else:
                print("\nInvalid choice. Please choose 'I', 'dealer', or 'back'.")
    
    def get_action_choice(self):
        while True:
            choose2 = input("\nPlease action(shoot/tools/exit): ")
            if choose2 in ["shoot", "tools","exit"]:
                return choose2
            else:
                print("\nInvalid action. Please choose 'shoot', 'tools' or 'exit'.")

    def check_player(self,player,flag):
        if player.hp <= 0:
            dead_list.append(player)
            print("\n{} failed.Level is {}".format(player.name,player.level))
            remove_player_by_name(player.name,player_list)
            self.save()
            flag = False
            return True
        return False
    
    def check_computer(self,player,player1):
        if player.hp <= 0:
            print("\nYou win")
            player1.level += 1
            player.level += 1
            player1.hp = 4
            player.hp = 4
            player1.tools = []
            player.tools = []
            print("Now:")
            print(player1)
            print(player)
            print("")
            self.save()
            return True
        return False
    
    def check_gun(self,gun,player,computer1):
        if gun.order == []:
            gun.reload()
            print(player)
            print(computer1)

    def run_game(self):
        """游戏主循环"""
        self.read()
        the_one = None
        the_gun = gun()
        if player_list != []:
            choose1 = input("\nnew game or use player in list(new/list))")
        while the_one == None:
            if player_list == [] or choose1 == "new":
                create(player_list)
            for p in player_list:
                print(p)
            choose1 = input("\nChoose your player: ")
            for gamer in player_list:
                if gamer.name == choose1:
                    the_one = gamer
                    break
        print("\nGame start")
        if computer_list == []:
            computer_list.append(player("Cheese Sandwich"))
        computer = computer_list[0]
        Flag = True
        while Flag:
            self.check_gun(the_gun,the_one,computer)
            if self.check_player(the_one,Flag):
                computer.level = 0
                break
            if self.check_computer(computer,the_one):
                continue
            while Flag:
                self.check_gun(the_gun,the_one,computer)
                choose2 = self.get_action_choice() #加个检查还有退出使用函数封装减少浪费过去式
                if choose2 == "shoot":
                    self.check_gun(the_gun,the_one,computer)
                    choose3 = self.get_shoot_choice()
                    if choose3 is None:
                        continue
                    elif choose3 == "I":
                        print("\nYou shoot yourself")
                        result = the_gun.shoot(the_one,computer)                        
                        if not result:
                            continue
                    elif choose3 == "dealer":
                        print("\nYou shoot the dealer")
                        result = the_gun.shoot(computer,the_one)
                elif choose2 == "tools":
                    print("正在施工")
                    continue
                elif choose2 =="exit":
                    self.save()
                    Flag = False
                break
            self.check_gun(the_gun,the_one,computer)
            if self.check_player(the_one,Flag):
                computer.level = 0
                break
            if self.check_computer(computer,the_one):
                continue
            while Flag:
                self.check_gun(the_gun,the_one,computer)
                #之后是人机的回合
                if the_gun.order == []:
                    the_gun.reload()
                n = sum(1 for value in the_gun.order if value)
                m = sum(1 for value in the_gun.order if not value)
                s = m+n
                if n/s > 0.72:
                    decide = True #向对方射击
                elif n/s < 0.24:
                    decide = False #向自己射击
                else:
                    decide = random.choice([True,False])
                if not decide:
                    print("\nDealer shoot himself")                       
                    result = the_gun.shoot(computer,the_one)
                    if not result:
                        continue           
                elif decide:
                    print("\nDealer shoot you")        
                    result = the_gun.shoot(the_one,computer)
                break

if __name__ == "__main__":
    player_list,dead_list,computer_list = [],[],[]
    main = lunpandu()
    player_list,dead_list,computer_list = main.read()
    while True:
        main.menu()
