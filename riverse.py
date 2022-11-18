# -*- coding:utf-8 -*-
import tkinter
import tkinter.messagebox
import numpy as np


# キャンバスの横方向・縦方向のサイズ（px）
# 400*2(オセロを角度表示) と間の隙間の10px
CANVAS_WIDTH_SIZE = 810
CANVAS_HEIGHT_SIZE = 400
# オセロと角度表示で半分ずつ
OTHELLO_SISE = 400

# 横方向・縦方向のマスの数
NUM_SQUARE = 8

#量子ビットの設定
n_qubit = 8


# 色の設定
BOARD_COLOR = 'green' # 盤面の背景色
YOUR_COLOR = 'black' # あなたの石の色
COM_COLOR = 'white' # 相手の石の色
PLACABLE_COLOR = 'yellow' # 次に石を置ける場所を示す色

# 角度の設定
base_theta = np.pi / 2
# 70度
theta_0 = np.pi / (180 / 70)

# プレイヤーを示す値
YOU = 1
COM = 2


class Othello():
    def __init__(self, master):
        '''コンストラクタ'''
        self.master = master # 親ウィジェット
        self.player = YOU # 次に置く石の色
        self.board = None # 盤面上の石を管理する２次元リスト
        self.color = { # 石の色を保持する辞書
            YOU : YOUR_COLOR,
            COM : COM_COLOR
        }
        # ウィジェットの作成
        self.createWidgets()
        # イベントの設定
        self.setEvents()
        # オセロゲームの初期化
        self.initOthello()
    def createWidgets(self):
        '''ウィジェットを作成・配置する'''
        # キャンバスの作成
        self.canvas = tkinter.Canvas(
            self.master,
            bg=BOARD_COLOR,
            width=CANVAS_WIDTH_SIZE+1, # +1は枠線描画のため
            height=CANVAS_HEIGHT_SIZE+1, # +1は枠線描画のため
            highlightthickness=0
        )
        self.canvas.pack(padx=10, pady=10)
    def setEvents(self):
        '''イベントを設定する'''

        # キャンバス上のマウスクリックを受け付ける
        self.canvas.bind('<ButtonPress>', self.click)

    def initOthello(self):
        '''ゲームの初期化を行う'''

        # 盤面上の石を管理する２次元リストを作成（最初は全てNone）
        self.board = [[None] * NUM_SQUARE for i in range(NUM_SQUARE)]
        # 石の角度を管理する2次元リストを作成（最初は90度（重ね合わせ））
        self.angle = [[np.pi / 2] * NUM_SQUARE for i in range(NUM_SQUARE)]

        # １マスのサイズ（px）を計算
        self.square_size = OTHELLO_SISE // NUM_SQUARE

        # マスを描画
        for y in range(NUM_SQUARE):
            for x in range(NUM_SQUARE):
                # 長方形の開始・終了座標を計算
                xs = x * self.square_size
                ys = y * self.square_size
                xe = (x + 1) * self.square_size
                ye = (y + 1) * self.square_size
                
                # 長方形を描画
                tag_name = 'square_' + str(x) + '_' + str(y)
                self.canvas.create_rectangle(
                    xs, ys,
                    xe, ye,
                    tag=tag_name
                )
        # あなたの石の描画位置を計算
        your_init_pos_1_x = NUM_SQUARE // 2
        your_init_pos_1_y = NUM_SQUARE // 2
        your_init_pos_2_x = NUM_SQUARE // 2 - 1
        your_init_pos_2_y = NUM_SQUARE // 2 - 1

        your_init_pos = (
            (your_init_pos_1_x, your_init_pos_1_y),
            (your_init_pos_2_x, your_init_pos_2_y)
        )
        # 計算した描画位置に石（円）と角度を描画
        for x, y in your_init_pos:
            self.drawDisk(x, y, self.color[YOU])
            self.registerAngle(x, y, self.color[YOU])
            self.printAngle(x, y)
        # 対戦相手の石の描画位置を計算
        com_init_pos_1_x = NUM_SQUARE // 2 - 1
        com_init_pos_1_y = NUM_SQUARE // 2
        com_init_pos_2_x = NUM_SQUARE // 2
        com_init_pos_2_y = NUM_SQUARE // 2 - 1

        com_init_pos = (
            (com_init_pos_1_x, com_init_pos_1_y),
            (com_init_pos_2_x, com_init_pos_2_y)
        )
        # 計算した描画位置に石（円）と角度を描画
        for x, y in com_init_pos:
            self.drawDisk(x, y, self.color[COM])
            self.registerAngle(x, y, self.color[COM])
            self.printAngle(x, y)

        # 最初に置くことができる石の位置を取得
        placable = self.getPlacable()

        # その位置を盤面に表示
        self.showPlacable(placable)

        # 角度表示マスを描画
        for y in range(NUM_SQUARE):
            for x in range(NUM_SQUARE):
                # 長方形の開始・終了座標を計算
                # 10は余白
                axs = x * self.square_size + OTHELLO_SISE + 10
                axe = (x + 1) * self.square_size + OTHELLO_SISE + 10
                ays = y * self.square_size
                aye = (y + 1) * self.square_size

                # 長方形を描画
                tag_name = 'square_angle_' + str(x) + '_' + str(y)
                self.canvas.create_rectangle(
                    axs, ays,
                    axe, aye,
                    tag=tag_name
                )

    def drawDisk(self, x, y, color):
        '''(x,y)に色がcolorの石を置く（円を描画する）'''

        # (x,y)のマスの中心座標を計算
        center_x = (x + 0.5) * self.square_size
        center_y = (y + 0.5) * self.square_size

        # 中心座標から円の開始座標と終了座標を計算
        xs = center_x - (self.square_size * 0.8) // 2
        ys = center_y - (self.square_size * 0.8) // 2
        xe = center_x + (self.square_size * 0.8) // 2
        ye = center_y + (self.square_size * 0.8) // 2
        
        # 円を描画する
        tag_name = 'disk_' + str(x) + '_' + str(y)
        self.canvas.create_oval(
            xs, ys,
            xe, ye,
            fill=color,
            tag=tag_name
        )

        # 描画した円の色を管理リストに記憶させておく
        self.board[y][x] = color

    def printAngle(self, x, y):
        '''角度をマスに表示する'''
        # (x,y)のマスの中心座標を計算
        center_x = (x + 0.5) * self.square_size + OTHELLO_SISE + 10
        center_y = (y + 0.5) * self.square_size

        tag_name = 'angle_' + str(x) + '_' + str(y)
        self.canvas.create_text(
                center_x, center_y,
                # 一の位が9になってしまうのを繰り上げる
                text=round(int((np.degrees(self.angle[y][x]))), -1),
                fill="white",
                tag=tag_name
        )

    def registerAngle(self, x, y, color):
        '''新しい石を置いたときに角度を登録する'''
        if color == YOUR_COLOR:
            self.angle[y][x] += base_theta
        else:
            self.angle[y][x] -= base_theta

    def changeAngle(self, x, y, surroundedColor, surroundedDiskNum):
        # 一桁めが9になる
        if surroundedColor == "black":
            self.angle[y][x] += theta_0 * surroundedDiskNum
        else:
            self.angle[y][x] -= theta_0 * surroundedDiskNum

    def getPlacable(self):
        '''次に置くことができる石の位置を取得'''

        placable = []

        for y in range(NUM_SQUARE):
            for x in range(NUM_SQUARE):
                # (x,y) の位置のマスに石が置けるかどうかをチェック
                if self.checkPlacable(x, y):
                    # 置けるならその座標をリストに追加
                    placable.append((x, y))
        return placable

    def checkPlacable(self, x, y):
        '''(x,y)に石が置けるかどうかをチェック'''
        # その場所に石が置かれていれば置けない
        if self.board[y][x] != None:
            return False

        if self.player == YOU:
            other = COM
        else:
            other = YOU

        # (x,y)座標から縦横斜め全方向に対して相手の石が裏返せるかどうかを確認
        for j in range(-1, 2):
            for i in range(-1, 2):

                # 真ん中方向はチェックしてもしょうがないので次の方向の確認に移る
                if i == 0 and j == 0:
                    continue

                # その方向が盤面外になる場合も次の方向の確認に移る
                if x + i < 0 or x + i >= NUM_SQUARE or y + j < 0 or y + j >= NUM_SQUARE:
                    continue

                # 隣が相手の色でなければその方向に石を置いても裏返せない
                if self.board[y + j][x + i] != self.color[other]:
                    continue

                # 置こうとしているマスから遠い方向へ１マスずつ確認
                for s in range(2, NUM_SQUARE):
                    # 盤面外のマスはチェックしない
                    if x + i * s >= 0 and x + i * s < NUM_SQUARE and y + j * s >= 0 and y + j * s < NUM_SQUARE:
                        
                        if self.board[y + j * s][x + i * s] == None:
                            # 自分の石が見つかる前に空きがある場合
                            # この方向の石は裏返せないので次の方向をチェック
                            break

                        # その方向に自分の色の石があれば石が裏返せる
                        if self.board[y + j * s][x + i * s] == self.color[self.player]:
                            return True
        
        # 裏返せる石がなかったので(x,y)に石は置けない
        return False

    def showPlacable(self, placable):
        '''placableに格納された次に石が置けるマスの色を変更する'''

        for y in range(NUM_SQUARE):
            for x in range(NUM_SQUARE):

                # fillを変更して石が置けるマスの色を変更
                tag_name = 'square_' + str(x) + '_' + str(y)
                if (x, y) in placable:
                    self.canvas.itemconfig(
                        tag_name,
                        fill=PLACABLE_COLOR
                    )

                else:
                    self.canvas.itemconfig(
                        tag_name,
                        fill=BOARD_COLOR
                    )

    def click(self, event):
        '''盤面がクリックされた時の処理'''

        if self.player != YOU:
            # COMが石を置くターンの時は何もしない
            return

        # クリックされた位置がどのマスであるかを計算
        x = event.x // self.square_size
        y = event.y // self.square_size

        if self.checkPlacable(x, y):
            # 角度
            self.registerAngle(x, y, self.color[self.player])
            self.printAngle(x, y)

            # 次に石を置けるマスであれば石を置く
            self.place(x, y, self.color[self.player])

    def place(self, x, y, color):
        '''(x,y)に色がcolorの石を置く'''

        # (x,y)に石が置かれた時に裏返る石を裏返す
        self.reverse(x, y)

        # (x,y)に石を置く（円を描画する）
        self.drawDisk(x, y, color)

        # 次に石を置くプレイヤーを決める
        before_player = self.player
        self.nextPlayer()
        
        if before_player == self.player:
            # 前と同じプレイヤーであればスキップされたことになるのでそれを表示
            if self.player != YOU:
                tkinter.messagebox.showinfo('結果', 'あなたのターンをスキップしました')
            else:
                tkinter.messagebox.showinfo('結果', 'COMのターンをスキップしました')

        elif not self.player:
            # 次に石が置けるプレイヤーがいない場合はゲーム終了
            self.showResult()
            return

        # 次に石がおける位置を取得して表示
        placable = self.getPlacable()
        self.showPlacable(placable)

        if self.player == COM:
            # 次のプレイヤーがCOMの場合は1秒後にCOMに石を置く場所を決めさせる
            self.master.after(1000, self.com)

    def reverse(self, x, y):
        '''(x,y)に石が置かれた時に裏返す必要のある石を裏返す'''

        if self.board[y][x] != None:
            # (x,y)にすでに石が置かれている場合は何もしない
            return

        if self.player == COM:
            other = YOU
        else:
            other = COM

        for j in range(-1, 2):
            for i in range(-1, 2):
                # 真ん中方向はチェックしてもしょうがないので次の方向の確認に移る
                if i == 0 and j == 0:
                    continue

                if x + i < 0 or x + i >= NUM_SQUARE or y + j < 0 or y + j >= NUM_SQUARE:
                    continue

                # 隣が相手の色でなければその方向で裏返せる石はない
                if self.board[y + j][x + i] != self.color[other]:
                    continue

                # 置こうとしているマスから遠い方向へ１マスずつ確認
                for s in range(2, NUM_SQUARE):
                    # 盤面外のマスはチェックしない
                    if x + i * s >= 0 and x + i * s < NUM_SQUARE and y + j * s >= 0 and y + j * s < NUM_SQUARE:
                        
                        if self.board[y + j * s][x + i * s] == None:
                            # 自分の石が見つかる前に空きがある場合
                            # この方向の石は裏返せないので次の方向をチェック
                            break

                        # その方向に自分の色の石があれば石が裏返せる
                        if self.board[y + j * s][x + i * s] == self.color[self.player]:
                            for n in range(1, s):
                                # 盤面の石の管理リストを石を裏返した状態に更新
                                self.board[y + j * n][x + i * n] = self.color[self.player]

                                # 石の色を変更することで石の裏返しを実現
                                tag_name = 'disk_' + str(x + i * n) + '_' + str(y + j * n)
                                self.canvas.itemconfig(
                                    tag_name,
                                    fill=self.color[self.player]
                                )

                                # 角度を変更
                                tag_name = 'angle_' + str(x + i * n) + '_' + str(y + j * n)
                                self.changeAngle(x + i * n, y + j * n, self.color[self.player], s-1)
                                self.canvas.itemconfig(
                                        tag_name,
                                        text=round(int(np.degrees(self.angle[y + j * n][x + i * n])), -1))

                            break

    def nextPlayer(self):
        '''次に石を置くプレイヤーを決める'''

        before_player = self.player

        # 石を置くプレイヤーを切り替える
        if self.player == YOU:
            self.player = COM
        else:
            self.player = YOU

        # 切り替え後のプレイヤーが石を置けるかどうかを確認
        placable = self.getPlacable()

        if len(placable) == 0:
            # 石が置けないのであればスキップ
            self.player = before_player

            # スキップ後のプレイヤーが石を置けるかどうかを確認
            placable = self.getPlacable()

            if len(placable) == 0:
                # それでも置けないのであれば両者とも石を置けないということ
                self.player = None

    def showResult(self):
        '''ゲーム終了時の結果を表示する'''

        # それぞれの色の石の数を数える
        num_your = 0
        num_com = 0

        for y in range(NUM_SQUARE):
            for x in range(NUM_SQUARE):
                if self.board[y][x] == YOUR_COLOR:
                    num_your += 1
                elif self.board[y][x] == COM_COLOR:
                    num_com += 1

        # 確率振幅を合計する
        prop_your = 0
        prop_com = 0

        for i in range(NUM_SQUARE):
            for x in range(NUM_SQUARE):
                prop_your += (np.cos((self.angle[i][x])/2))**2
                prop_com += (np.sin((self.angle[i][x])/2))**2

        prop_your = round(prop_your, 2)
        prop_com = round(prop_com, 2)

        # 結果をメッセージボックスで表示する
        tkinter.messagebox.showinfo('結果', 'あなた' + str(num_your) + '：COM' + str(num_com))
        tkinter.messagebox.showinfo('角度の結果','あなた' + str(prop_your) + ':COM' + str(prop_com))

    def com(self):
        '''COMに石を置かせる'''

        # 石が置けるマスを取得
        placable = self.getPlacable()

        # 最初のマスを次に石を置くマスとする
        x, y = placable[0]

        # 角度を表示
        self.registerAngle(x, y, COM_COLOR)
        self.printAngle(x, y)

        # 石を置く
        self.place(x, y, COM_COLOR)


# スクリプト処理ここから
app = tkinter.Tk()
app.title('othello')
othello = Othello(app)
app.mainloop()
