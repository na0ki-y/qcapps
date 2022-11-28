'''
https://camp.trainocate.co.jp/magazine/streamlit-web/
'''
import numpy as np
import streamlit as st
import random
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit import Aer
from qiskit.visualization import array_to_latex



# From: https://stackoverflow.com/questions/39922967/python-determine-tic-tac-toe-winner


def checkWin(board):
   pass

NUM_SQUARE=4

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
                                kawaru(x + i * n,y + j * n,st.session_state.next_player,theta_0*(s-1))

                                
                            break

random_l=[-1,0,0,0,1]
def kawaru(x,y,which,kakudo):
    '''裏返ったときに色変更と角度を変更する'''
    st.session_state.board[x][y]=color_dic[which]
    if random.random()>0.95:
        if which == YOU:
            st.session_state.angle[x][y] += kakudo
        else:
            st.session_state.angle[x][y] -= kakudo
def oku(x,y,which):
    '''新しい石を置いたときに色変更と角度を登録する'''
    #drawDisk
    reverse(x,y)
    st.session_state.board[x][y]=color_dic[which]
    if which == YOU:
        st.session_state.angle[x][y] += base_theta
    else:
        st.session_state.angle[x][y] -= base_theta

def showResult():
        '''ゲーム終了時の結果を表示する'''

        # それぞれの色の石の数を数える
        num_your = 0
        num_com = 0

        for y in range(NUM_SQUARE):
            for x in range(NUM_SQUARE):
                if st.session_state.board[y][x] == YOUR_COLOR:
                    num_your += 1
                elif st.session_state.board[y][x] == COM_COLOR:
                    num_com += 1
        simple_winner="Player2○"
        if num_your>num_com:
            simple_winner="Player1●"
        # 確率振幅を合計する
        prop_your = 0
        prop_com = 0

        for y in range(NUM_SQUARE):
            for x in range(NUM_SQUARE):
                prop_your += (np.cos((st.session_state.angle[y][x])/2))**2
                prop_com += (np.sin((st.session_state.angle[y][x])/2))**2

        prop_your = round(prop_your, 2)
        prop_com = round(prop_com, 2)
        q_winner="Player2○"
        if prop_your>prop_com:
            q_winner="Player1●"
        
        #qiskit
        # 角度を量子シュミレータを使って計算
        qc = QuantumCircuit(0)
        qr = QuantumRegister(NUM_SQUARE*NUM_SQUARE)
        qc.add_register(qr)
        qc.h(qr)
        for y in range(NUM_SQUARE):
            for x in range(NUM_SQUARE):
                qc.ry(st.session_state.angle[y][x], qr[y*NUM_SQUARE+x])
        cr = ClassicalRegister(NUM_SQUARE*NUM_SQUARE,'creg')
        qc.add_register(cr)                             #測定後の0or1を保存する従来のレジスタ   確率ではない
        qc.measure(qr,cr)                         #観測する
        sim = Aer.get_backend('qasm_simulator')        #実際に動かした時のシミュレータ
        res = sim.run(qc, shots = 1).result()    
        ans=list(res.get_counts().keys())[0]
        q_num_your=ans.count("1")
        q_num_com=ans.count("0")
        q_simple_winner="Player2○"
        if q_num_your>q_num_com:
            q_simple_winner="Player1●"
        




  
        st.session_state.game_result ={"YOU_num":num_your,"COM_num":num_com,"YOU_angle":prop_your,"COM_angle":prop_com,"q_YOU_num":q_num_your,"q_COM_num":q_num_com,"Simple_winner":simple_winner,"Q_winner":q_winner,"q_Simple_winner":q_simple_winner,}

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
def init_syori():
    st.session_state.mode_com ="YOU v.s.COM"

    st.session_state.next_player =COM 
    st.session_state.placable = None
    st.session_state.message=init_message
    st.session_state.game_result=None
    st.session_state.board = np.full((NUM_SQUARE, NUM_SQUARE),BOARD_COLOR, dtype=str)
    # 石の角度を管理する2次元リストを作成（最初は90度（重ね合わせ））
    st.session_state.angle = np.full((NUM_SQUARE, NUM_SQUARE), np.pi / 2, dtype=float)
    mannaka=int(NUM_SQUARE/2)
    oku(mannaka,mannaka,YOU)
    oku(mannaka-1,mannaka-1,YOU)
    oku(mannaka-1,mannaka,COM)
    oku(mannaka,mannaka-1,COM)
def com():
    # 石が置けるマスを取得
    st.session_state.placable = getPlacable()

    # 最初のマスを次に石を置くマスとする
    if len(st.session_state.placable)!=0:
        x, y = st.session_state.placable[0]
        oku(x,y,YOU)
    st.session_state.next_player = (
                YOU  if st.session_state.next_player ==COM  else COM
                )


def main():
    st.header('Q-Reversi')
    st.caption("[QC4U](https://altema.is.tohoku.ac.jp/QC4U/) Group4(Quantum Force)")

    #https://github.com/streamlit/release-demos/blob/0.84/0.84/demos/tic_tac_toe.py
    

    # Initialize state.
    if "board" not in st.session_state:
        init_syori()
    
    #if st.session_state.mode_com=='YOU v.s.COM':
    #    st.write("あなたの色:"+color_dic[st.session_state.next_player])
    
    #    st.write("次は:Player"+str(st.session_state.next_player)+color_dic[st.session_state.next_player])

    #if st.button("モード変更"):
    #   st.session_state.mode_com=st.radio(
    #    "Mode Selection",
    #    ('YOU v.s.COM', 'Player1 v.s. Player2'))
    st.write("次は:Player"+str(st.session_state.next_player)+color_dic[st.session_state.next_player])
    st.write(st.session_state.message)

        # Define callbacks to handle button clicks.
    st.session_state.placable = getPlacable()
    showPlacable(st.session_state.placable)
    if len(st.session_state.placable)==0:
        #skip
        st.session_state.next_player = (
                YOU  if st.session_state.next_player ==COM  else COM
                )
        st.session_state.placable = getPlacable()
        if len(st.session_state.placable)==0:
            #game end
            showResult()



    def handle_click(i, j):#click
            if checkPlacable(i, j):
                st.session_state.message=init_message
                # TODO: Handle the case when nobody wins but the game is over!
                oku(i,j,st.session_state.next_player)

                st.session_state.next_player = (
                YOU  if st.session_state.next_player ==COM  else COM
                )
                
            else:
                st.session_state.message="注意！そこにはおけません"
            #if st.session_state.mode_com=="YOU v.s.COM":
            #    com()
                

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


    if st.session_state.game_result!=None:
        #st.session_state.game_result ={"YOU_num":num_your,"COM_num":num_com,"YOU_angle":prop_your,"COM_angle":prop_com,"Simple_winner":simple_winner,"Q_winner":q_winner}
        st.balloons()
        st.success("Simple Reversi:"+st.session_state.game_result["Simple_winner"]+"(you:{},com:{})".format(st.session_state.game_result["YOU_num"],st.session_state.game_result["COM_num"]))
        st.success("Q-Reversi:"+st.session_state.game_result["Q_winner"]+"(you:{},com:{})".format(st.session_state.game_result["YOU_angle"],st.session_state.game_result["COM_angle"]))
        st.success("Q-Reversi_v2:"+st.session_state.game_result["q_Simple_winner"]+"(you:{},com:{})".format(st.session_state.game_result["q_YOU_num"],st.session_state.game_result["q_COM_num"]))



    ckbx_angle = st.checkbox("角度を確認する") #引数に入れることでboolを返す
    if ckbx_angle:
        st.table(st.session_state.angle)#,0.1,0.1)
        #st.table(np.round(st.session_state.angle, 2))
    #if st.checkbox('はじめから'):
    #    st.info('本当に、はじめからにしますか？', icon="ℹ️")
    #    if st.checkbox('はい。'):
    #        init_syori()
    st.caption("[View source code](https://github.com/na0ki-y/qcapps)")
if __name__ == '__main__':
    main()