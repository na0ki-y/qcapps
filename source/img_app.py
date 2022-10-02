'''
https://camp.trainocate.co.jp/magazine/streamlit-web/
'''
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
            device,model,transform=pytorch_pretrained.prepara()
            #img = Image.open("./image/irasutoya_character_apple.png")
            inputs=pytorch_pretrained.mycovert(load_image(image_file),device,transform)
            eval_out=pytorch_pretrained.myeval(inputs,model,)
            st.markdown("アップロードしたファイルの推論結果")
            for o in eval_out:
                st.markdown(o)

    st.markdown("# Pytorch")
    st.markdown("サーバにあるファイルの推論結果")
    device,model,transform=pytorch_pretrained.prepara()
    img = Image.open("./image/irasutoya_character_apple.png")
    st.image(img,width=250)
    inputs=pytorch_pretrained.mycovert(img,device,transform)
    eval_out=pytorch_pretrained.myeval(inputs,model,)
    for o in eval_out:
        st.markdown(o)
    
if __name__ == '__main__':
    main()