'''
https://camp.trainocate.co.jp/magazine/streamlit-web/
'''
import numpy as np
import streamlit as st
from PIL import Image
import sys
import pathlib
# ひとつ上の階層の絶対パスを取得
parent_dir = str(pathlib.Path(__file__).parent.parent.resolve())
# モジュール検索パスに，ひとつ上の階層の絶対パスを追加
sys.path.append(parent_dir)
from source import pytorch_pretrained 
#import pytorch_pretrained 


# From: https://stackoverflow.com/questions/39922967/python-determine-tic-tac-toe-winner


def checkWin(board):
   pass

NUM_SQUARE=8#6

YOUR_COLOR = "●" # あなたの石の色
COM_COLOR = "○" # 相手の石の色
PLACABLE_COLOR = '□' # 次に石を置ける場所を示す色
BOARD_COLOR="＿"
# 角度の設定
base_theta = np.pi / 2
# 70度
theta_0 = np.pi / (180 / 70)

# プレイヤーを示す値
YOU = 1
COM = 2

color_dic = { # 石の色を保持する辞書
            YOU : YOUR_COLOR,
            COM : COM_COLOR
        }

def registerAngle(x, y, which):
        '''新しい石を置いたときに角度を登録する'''
        if which == YOU:
            st.session_state.angle[x][y] += base_theta
        else:
            st.session_state.angle[x][y] -= base_theta
def kawaruAngle(x, y, which,kakudo):
        '''裏返ったときに角度を変更する'''
        if which == YOU:
            st.session_state.angle[x][y] += kakudo
        else:
            st.session_state.angle[x][y] -= kakudo
def reverse(x, y):
        '''(x,y)に石が置かれた時に裏返す必要のある石を裏返す'''
        # (x,y)にすでに石が置かれている場合は何もしない
        if st.session_state.board[x][y] == YOUR_COLOR or st.session_state.board[x][y] == COM_COLOR:
            return

        if st.session_state.next_player == COM:
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
                if st.session_state.board[x + i][y + j] != color_dic[other]:
                    continue

                # 置こうとしているマスから遠い方向へ１マスずつ確認
                for s in range(2, NUM_SQUARE):
                    # 盤面外のマスはチェックしない
                    if x + i * s >= 0 and x + i * s < NUM_SQUARE and y + j * s >= 0 and y + j * s < NUM_SQUARE:
                        
                        if st.session_state.board[x + i * s][y + j * s] == BOARD_COLOR or st.session_state.board[x + i * s][y + j * s] == PLACABLE_COLOR:
                            # 自分の石が見つかる前に空きがある場合
                            # この方向の石は裏返せないので次の方向をチェック
                            break

                        # その方向に自分の色の石があれば石が裏返せる
                        if st.session_state.board[x + i * s][y + j * s] == color_dic[st.session_state.next_player]:
                            for n in range(1, s):
                                # 盤面の石の管理リストを石を裏返した状態に更新
                                kawaru(x + i * n,y + j * n,st.session_state.next_player,theta_0*s-1/NUM_SQUARE)

                                
                            break
def kawaru(r,c,which,kakudo):
    st.session_state.board[r][c]=color_dic[which]
    kawaruAngle(r,c,which,kakudo)
def oku(r,c,which):
    #drawDisk
    reverse(r,c)
    st.session_state.board[r][c]=color_dic[which]
    registerAngle(r,c,which)

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


def checkPlacable(x, y):
        '''(x,y)に石が置けるかどうかをチェック'''
        # その場所に石が置かれていれば置けない
        if st.session_state.board[x][y] == YOUR_COLOR or st.session_state.board[x][y] == COM_COLOR:
            return False

        if st.session_state.next_player == YOU:
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
                if st.session_state.board[x + i][y + j] != color_dic[other]:
                    continue

                # 置こうとしているマスから遠い方向へ１マスずつ確認
                for s in range(2, NUM_SQUARE):
                    # 盤面外のマスはチェックしない
                    if x + i * s >= 0 and x + i * s < NUM_SQUARE and y + j * s >= 0 and y + j * s < NUM_SQUARE:
                        
                        if st.session_state.board[x + i * s][y + j * s] == BOARD_COLOR or st.session_state.board[x + i * s][y + j * s] == PLACABLE_COLOR:
                            # 自分の石が見つかる前に空きがある場合
                            # この方向の石は裏返せないので次の方向をチェック
                            break

                        # その方向に自分の色の石があれば石が裏返せる
                        if st.session_state.board[x + i * s][y + j * s] == color_dic[st.session_state.next_player]:
                            return True
        
        # 裏返せる石がなかったので(x,y)に石は置けない
        return False
def showPlacable(placable):
    '''placableに格納された次に石が置けるマスの色を変更する'''

    for x in range(NUM_SQUARE):
        for y in range(NUM_SQUARE):

            # fillを変更して石が置けるマスの色を変更
            # その場所に石が置かれていれば置けない
            
            if st.session_state.board[x][y] == YOUR_COLOR or st.session_state.board[x][y] == COM_COLOR:
                continue
            
            if (x, y) in placable:
                st.session_state.board[x][y] = PLACABLE_COLOR
            else:
                st.session_state.board[x][y] = BOARD_COLOR

def getPlacable():
    '''次に置くことができる石の位置を取得'''

    placable = []

    for y in range(NUM_SQUARE):
        for x in range(NUM_SQUARE):
            # (x,y) の位置のマスに石が置けるかどうかをチェック
            if checkPlacable(x, y):
                # 置けるならその座標をリストに追加
                placable.append((x, y))
    return placable

init_message=PLACABLE_COLOR+"の場所におけます。"
desp_cols=[0.2]*(NUM_SQUARE-1)+[0.9]#列の間隔　一番右だけ大きくするといい感じに左側に固まる！
def main():
    st.header('Q-Reversi')
    st.caption("[QC4U](https://altema.is.tohoku.ac.jp/QC4U/) Group4(Quantum Force)")

    #https://github.com/streamlit/release-demos/blob/0.84/0.84/demos/tic_tac_toe.py
    

    # Initialize state.
    if "board" not in st.session_state:
        st.session_state.next_player =COM 
        st.session_state.winner = None
        st.session_state.placable = None
        st.session_state.message=init_message
        st.session_state.board = np.full((NUM_SQUARE, NUM_SQUARE),BOARD_COLOR, dtype=str)
        # 石の角度を管理する2次元リストを作成（最初は90度（重ね合わせ））
        st.session_state.angle = np.full((NUM_SQUARE, NUM_SQUARE), np.pi / 2, dtype=float)
        mannaka=int(NUM_SQUARE/2)
        oku(mannaka,mannaka,YOU)
        oku(mannaka-1,mannaka-1,YOU)
        oku(mannaka-1,mannaka,COM)
        oku(mannaka,mannaka-1,COM)
        
    st.write("next player is:"+color_dic[st.session_state.next_player])
    st.write(st.session_state.message)

        # Define callbacks to handle button clicks.
    st.session_state.placable = getPlacable()
    showPlacable(st.session_state.placable)

    def handle_click(i, j):#click
        if not st.session_state.winner:
            if checkPlacable(i, j):
                st.session_state.message=init_message
                # TODO: Handle the case when nobody wins but the game is over!
                oku(i,j,st.session_state.next_player)

                st.session_state.next_player = (
                YOU  if st.session_state.next_player ==COM  else COM
                )
                winner = checkWin(st.session_state.board)
                if winner != BOARD_COLOR:
                    st.session_state.winner = winner
            else:
                st.session_state.message="注意！そこにはおけません"
                

    # Show one button for each field.
    for i, row in enumerate(st.session_state.board):
        cols = st.columns(desp_cols) 
            #bata_columsPlease replace st.beta_columns with st.columns. st.beta_columns will be removed after 2021-11-02.
        for j, field in enumerate(row):
            cols[j].button(
                field,
                key=f"{i}-{j}",
                on_click=handle_click,
                args=(i, j),
            )


    if st.session_state.winner:
        st.success(f"Congrats! {st.session_state.winner} won the game! 🎈")

    ckbx_angle = st.checkbox("角度を確認する") #引数に入れることでboolを返す

    if ckbx_angle:
        st.table(st.session_state.angle)#,0.1,0.1)

    
if __name__ == '__main__':
    main()