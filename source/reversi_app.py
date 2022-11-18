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

player_one="●"
player_two="○"

board_num=8#6
desp_cols=[0.2]*(board_num-1)+[0.9]#列の間隔　一番右だけ大きくするといい感じに左側に固まる！
def main():
    st.header('Q-Reversi')
    st.caption("[QC4U](https://altema.is.tohoku.ac.jp/QC4U/) Group4(Quantum Force)")

    #https://github.com/streamlit/release-demos/blob/0.84/0.84/demos/tic_tac_toe.py
    

    # Initialize state.
    if "board" not in st.session_state:
        st.session_state.board = np.full((board_num, board_num), "＿", dtype=str)
        mannaka=int(board_num/2)
        st.session_state.board[mannaka][mannaka]=player_one
        st.session_state.board[mannaka-1][mannaka-1]=player_one
        st.session_state.board[mannaka][mannaka-1]=player_two
        st.session_state.board[mannaka-1][mannaka]=player_two
        st.session_state.next_player =player_two
        st.session_state.winner = None
    st.write("next player is:"+st.session_state.next_player)
        # Define callbacks to handle button clicks.
    def handle_click(i, j):
        if not st.session_state.winner:
            # TODO: Handle the case when nobody wins but the game is over!
            st.session_state.board[i, j] = st.session_state.next_player
            st.session_state.next_player = (
               player_one if st.session_state.next_player ==player_two else player_two
            )
            winner = checkWin(st.session_state.board)
            if winner != "＿":
                st.session_state.winner = winner

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



    
if __name__ == '__main__':
    main()