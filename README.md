# Overview
[mixamo](https://www.mixamo.com/)リグのアーマチュアボーン名をリネームし、特定のボーン（UpperChest）を削除する機能を提供します。このアドオンは、Mixamoからインポートしたアーマチュアのボーン名を整理し、アニメーションやリギング作業を効率化するために設計されています。


# Features

1. **ボーン名のリネーム**：
   - 「mixamorig:」接頭辞を削除。
   - 「Spine1」→「LowerChest」、「Spine2」→「UpperChest」。
   - 「Right」/「Left」→「_R」/「_L」（例: `RightArm` → `Arm_R`）。
   - 数値接尾辞（例: `.001`）を保持。

2. **UpperChestボーンの削除**：
   - ボーン名をリネーム後、UpperChestをLowerChest（「Chest」に改名）に統合して削除。
   - 関連メッシュの頂点グループのウェイトを統合。

# Usage

1. **インストール**：
   - スクリプトファイルをダウンロード。
   - Blenderの`編集` > `プリファレンス` > `アドオン`で「インストール」を選択し、ファイルを選択。
   - アドオンを有効化。

2. **操作**：
   - 3Dビューのサイドバーで`kjtools`タブを開く。
   - 「Rename Mixamorig」パネルでアーマチュアを選択。
   - ボタンをクリック：
     - **rename**: ボーン名をリネーム。
     - **dissolve**: ボーン名をリネームし、UpperChestを削除。

**注意**: アーマチュアを選択しないとエラーメッセージが表示されます。

詳細は
[note](https://note.com/preview/na94d5ed856a2?prev_access_key=06c01d8b5be97ea1075ee0c7c00fb0b7)
参照  


# Revision
v0.1: 2021/3/28  
first release  
  
v0.2: 2023/12/23  
詳細コード整理  
github設定  
  
v1.0: 2324/1/18  
Armature選択プロパティの追加  
dissolve Upperchest機能の追加  
スポイト選択の追加  
  
v1.1: 2324/2/4  
"COMMUNITY"変更  
細かいバグ修正  
github整理  
  
v1.2: 2325/4/16  
l_category変更  
  
v1.3: 2325/4/27  
ソースコード整理  
Readme整理  
