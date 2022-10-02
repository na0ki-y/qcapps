'''
https://camp.trainocate.co.jp/magazine/streamlit-web/
'''
import streamlit as st
from PIL import Image

def load_image(image_file):
	img = Image.open(image_file)
	return img

def main():
    st.title("Quantum Computer App ")
    st.markdown("[QC4U](https://altema.is.tohoku.ac.jp/QC4U/) Group4")
    st.markdown("# Upload image")
    image_file = st.file_uploader("Upload Images", type=["png","jpg","jpeg"])

    if image_file is not None:

            # To See details
            file_details = {"filename":image_file.name, "filetype":image_file.type,
                            "filesize":image_file.size}
            #st.write(file_details)

            # To View Uploaded Image
            st.image(load_image(image_file),width=250)

    st.markdown("# Other Sample")
    

    check = st.checkbox("チェックボックス") #引数に入れることでboolを返す

    if check:
        st.button("ボタン") #引数に入れるとboolで返す
        st.selectbox("メニューリスト", ("選択肢1", "選択肢2", "選択肢3")) #第一引数：リスト名、第二引数：選択肢
        st.multiselect("メニューリスト（複数選択可）", ("選択肢1", "選択肢2", "選択肢3")) #第一引数：リスト名、第二引数：選択肢、複数選択可
        st.radio("ラジオボタン", ("選択肢1", "選択肢2", "選択肢3")) #第一引数：リスト名（選択肢群の上に表示）、第二引数：選択肢
        st.text_input("文字入力欄") #引数に入力内容を渡せる
        st.text_area("テキストエリア") #引数に入力内容を渡せる
    st.sidebar.text_input("文字入力欄") #引数に入力内容を渡せる
    st.sidebar.text_area("テキストエリア")
if __name__ == '__main__':
    main()