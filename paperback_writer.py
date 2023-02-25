import MeCab
import markovify
import ipadic
import os

folder_path = 'C:/PythonWorkspace/paperback text/'

def main():
    # フォルダ内のすべての.txtファイルを読み込み
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.txt'):
            file_path = os.path.join(folder_path, file_name)
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()

    mecab = MeCab.Tagger(ipadic.MECAB_ARGS)

    # 上手く解釈できない文字列を定義しておく
    breaking_chars = ['(', ')', '[', ']', '"', "'", '《', '》']
    # 最終的に1文に収めるための変数
    splitted_text = ''

    for line in text:
        print(line)
        # lineの文字列をパースする
        parsed_nodes = mecab.parseToNode(line)

        while parsed_nodes:
            try:
                # 上手く解釈できない文字列は飛ばす
                if parsed_nodes.surface not in breaking_chars:
                    splitted_text += parsed_nodes.surface
                # 句読点以外であればスペースを付与して分かち書きをする
                if parsed_nodes.surface != '。' and parsed_nodes.surface != '、':
                    splitted_text += ' '
                # 句点が出てきたら文章の終わりと判断して改行を付与する
                if parsed_nodes.surface == '。':
                    splitted_text += '\n'
            except UnicodeDecodeError as error:
                print('Error : ', line)
            finally:
                # 次の形態素に上書きする。なければNoneが入る
                parsed_nodes = parsed_nodes.next

    print('解析結果 :\n', splitted_text)

    # マルコフ連鎖のモデルを作成
    model = markovify.NewlineText(splitted_text, state_size=2)

    # 文章を生成する
    sentence = model.make_sentence(tries=100)
    if sentence is not None:
        # 分かち書きされているのを結合して出力する
        print(''.join(sentence.split()))
    else:
        print('None')


if __name__ == "__main__":
    main()