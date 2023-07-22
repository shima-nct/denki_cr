# denki_cr

## 1. [remote-i2c] package を用いたサンプルについて
[remote-i2c] は Raspberry Pi の I2C を他の端末から制御することを可能とする python ライブラリパッケージです．
Raspberry Pi でサーバースクリプトを動かしておけば他の端末から Python スクリプトを用いて Raspberry Pi の I2C を操作できます．

remote-i2c のプロトコルは TCP を用いています．デフォルトの待受ポートは 5446 です。アドレスとデータをそのままバイナリのバイト列で送る至極簡単なプロトコルです。サーバーは受け取ったアドレス，データを I2C バスに送ります．
アドレスを指定してデータを読み込むことができます．

remote-i2c にはアクセス制限などの制御機構はありません．

なお remote-i2c バージョン 0.0.9 には `_read_byte_data()' メソッドがエラーになることと smbus2 パッケージへの依存情報がかけているバグがあります．これらのバグを修正したバージョンを[このレポジトリ](https://github.com/shima-nct/remote-i2c/tree/fix_lack_of_smbus2_dependency_and_write_word)に用意しておきました．

[remote-i2c]: https://pypi.org/project/remote-i2c/

### 1.1 [remote-i2c] package のインストール
#### Rasberry Pi OS, Kali Linux for Raspberry Pi へのインストール

remote-i2c バージョン 0.0.9 にはバグがあるので[このレポジトリ](https://github.com/shima-nct/remote-i2c/tree/fix_lack_of_smbus2_dependency_and_write_word)にある非公式パッケージをインストールします．

remote-i2c のインストール
```
sudo pip install https://github.com/shima-nct/remote-i2c/releases/download/v0.0.9_fix_write_word/remote_i2c-0.0.9-py3-none-any.whl
```

Kali LinuxなどDebianベースのLinuxで上記のパッケージインストールを行うと以下のようなエラーが表示される場合があります．

```
┌──(kali㉿kali)-[~/denki_cr]
└─$ sudo python3 -m pip  install https://github.com/shima-nct/remote-i2c/releases/download/v0.0.9_fix_write_word/remote_i2c-0.0.9-py3-none-any.whl
error: externally-managed-environment

× This environment is externally managed
╰─> To install Python packages system-wide, try apt install
    python3-xyz, where xyz is the package you are trying to
    install.
    
    If you wish to install a non-Debian-packaged Python package,
    create a virtual environment using python3 -m venv path/to/venv.
    Then use path/to/venv/bin/python and path/to/venv/bin/pip. Make
    sure you have python3-full installed.
    
    If you wish to install a non-Debian packaged Python application,
    it may be easiest to use pipx install xyz, which will manage a
    virtual environment for you. Make sure you have pipx installed.
    
    See /usr/share/doc/python3.11/README.venv for more information.

note: If you believe this is a mistake, please contact your Python installation or OS distribution provider. You can override this, at the risk of breaking your Python installation or OS, by passing --break-system-packages.
hint: See PEP 668 for the detailed specification.
```

この場合，エラーメッセージ内にも有るように`--break-system-packages`オプションを付けることでインスールすることができます．


#### Kali Linux へのインストール
本来は pip コマンドによるインストールで済むはずなのですが，エラーが生じてしまいます．このエラーは Kali Linux のアップデートで回避できます．

Kali Linux のアップデート
 ```
 sudo apt update
 sudo apt -y upgrade
 ```
remote-i2c のインストール
```
sudo pip install remote-i2c smbus2
```

### 1.2 サンプルスクリプト

以下のサンプルスクリプトは[based_remote_i2c](./based_remote_i2c/based_i2c)にあります．

#### `remote_i2c_server.py`
remote-i2c のドキュメントでも説明されているようにこのスクリプトを用いなくても以下のコマンでパッケージのデフォルトメソッドを実行することでサーバーとして動きます．
```
python -m remote_i2c
```

`remote_i2c_server.py` を用いる場合
```
python remote_i2c_server.py
```

#### `remote_i2c_client.py`
remote-i2c のドキュメントに掲載してあるサンプルだとうまく動きません．これはスクリプト内で用いられているメソッド `bus.write_byte_data(addr, reg, value)` がSMBus用だからです．`remote_i2c_client.py` ではI2C用の書き込みメソッドは `bus.write_byte(addr, value)` を用いています．

サーバーの IP アドレスを変数 `remote_i2c_host` に与えてください．コードを直接書き換えるか，コマンドラインオプション `--remote-host` で与えてください．以下の例はサーバーのIPアドレスが`10.1.109.123`の場合です．

```
python remote_i2c_client.py --remote-host 10.1.109.123
```

このスクリプトは Qwiic Quad Relay の全リレーの ON にし，1秒後に OFF にします．
この動作や他のデバイスに対応する場合はアドレスと書き込む値をデバイスの動作に合わせて変更してください．

スクリプトを一回だけ実行する方法
```
python remote_i2c_client.py --remote-host 10.1.109.123
```

スクリプトを繰り返し実行したい場合は，スクリプト内で for などの繰り返し文を用いるか、以下のように Shell 言語の while コマンドを用います．
```
while : ; do python remote_i2c_client.py --remote-host 10.1.109.123 ; done
```

#### `ex_pca9685_control.py`
サーボモータの回転角度は指令パルスのデューティ比で制御します．
サーボモーター[ASV-15-A]におけるパルス信号の仕様はリンク先の商品情報で確認してください．

SparkFun Auto PHAT のサーボーモーター制御は搭載されている[NXP PWM LED controller PCA9685]で行っています．このICに用意されているレジスタに値を書き込みPWMの周波数，デューティー比などを制御しています．
 `ex_pca9685_control.py` はこのレジスタを操作して回転角を5秒間隔で0°，45°，90°に変化させています．
 スクリプトのコメントに当該レジスタについて記載されている[PCA9685のデータシート]のページへのリンクを示しておきました．
 より複雑な動作をさせる場合はこれらの情報を参考にしてください．


スクリプトを一回だけ実行する方法
```
python ex_pca9685_control.py --remote-host 10.1.109.123
```

[NXP PWM LED controller PCA9685]: https://www.nxp.com/products/power-management/lighting-driver-and-controller-ics/ic-led-controllers/16-channel-12-bit-pwm-fm-plus-ic-bus-led-controller:PCA9685
[PCA9685のデータシート]: https://www.nxp.com/docs/en/data-sheet/PCA9685.pdf
[ASV-15-A]: http://www.robotsfx.com/robot/ASV-15.html

#### `ex_button_read.py`
Qwiic Buttonの押された瞬間，離した瞬間を表示します．

スクリプトを実行する方法
```
python ex_button_read.py --remote-host 10.1.109.123
```

Raspberry Piの`/boot/config.txt`  の最後に以下の一行を加えて再起動することが必要です．
```
dtparam=i2c_baudrate=50000
```

## 2. SparkFun Qwiic Package を利用したサンプルについて

Sparkfun が販売しているQwiicデバイスを制御するためにPythonのパッケージが用意されています．
以下に掲載したサンプルスクリプトの内，Raspberry Piで動かすサーバースクリプトはこのパッケージを用いてAuto pHATを制御しています．

### 2.1 [SparkFun Qwiic Python package] のインストール

```
sudo pip3 install sparkfun-qwiic
```

### 2.2 サンプルスクリプト

以下のサンプルスクリプトは[based_socket](./based_socket/)にあります．

#### `remote_auto_phat_server.py`

Auto pHAT のモータードライバーをリモートからコントロールするためのサーバースクリプトです．
[SparkFun Qwiic Python package]が必要です．
Socketを用いて作成した単純なTCP/IPサーバーです．
モーター制御の3つのパラメーター，モーター番号(0,1)，方向(0,1)，回転速度(0-255)の連想配列を受け取り，これらの値を`myMotor.set_drive(<モーター番号>, <方向>,  <速度>)`でモータードライバのメソッドに与えています．
このクライアントからサーバーへの通信は連想配列を[JSON]書式の文字列に変換して送っているのでWiresharkでキャプチャすれば簡単に通信内容を解釈することができます．

スクリプトを実行する方法
```
python remote_auto_phat_server.py --port 3354
```

#### `remote_auto_phat_client.py`

Auto pHAT のモータードライバーをリモートからコントロールします．
[Auto pHATのデモスクリプト]の様にモーターの速度を20-255の間で上下させています．

スクリプトを実行する方法．`--remote-host`オプションでサーバーのIPアドレスを指定します．
```
python remote_auto_phat_client.py --remote-host 10.1.101.12  --remote-port 3354
```

#### `etter.filter.auto_phat_socket`

`remote_auto_phat_client.py`と `remote_auto_phat_server.py`の間の通信を改ざんするettercapフィルターです．
回転方向を反転（0から1）にし，さらにスピードを最速（最大値の255）に改ざんします．
このコードを`etterfilter`でコンパイルし，出力されたファイルをARP Poinsoningを行っている`ettercap`や`ettercap-graphical`でfilterとして読み込ませることで働きます．

##### etter.filter.auto_phat_socketのコンパイル方法
```
etterfilter etter.filter.auto_phat_socket
```

`-o`オプションで出力ファイル名を指定していなければデフォルトで`filter.ef`として出力されます．

##### ettercapでフィルタを読み込ませるには

`ettercap-graphical`で読み込ませるには，まずARP Poisoningを実行している状態で，3点リーダーアイコン→「Filters」→「Load a filter...」で開くエクスプローラーで`filter.ef`を選択し，右上「OK」をクリックします．

このエクスプローラーで`filter.ef`を読み込ませる際に，二つの注意点があります．

一つ目の注意点はホームディレクトリに他のユーザーの読み込み権限を付けることです．
Kali Linuxのデフォルトアカウント`kali`のホームディレクトリには他のユーザー以外の読み込み権限が付けられていません．`ettercap-graphical`は`nobody`ユーザー権限で実行されるため，このままでは`kali`のホームディレクトリ以下にあるファイルを読み込むことができません．なお，ホームディレクトリ以下のディレクトリには他ユーザーの読み込み権限が付けられているので，読み込み権限を付与するのはホームディレクトリだけでかまいません．

ホームディレクトリに他のユーザーの読み込み権限を付与する方法
```
chmod go+rx ~
```
ここで`~`はホームディレクトリのパスを表す短縮表現です．`g`やグループユーザー，`o`は他のユーザーを表しています．`r`は読み込み権限，`x`は実行権限を表しています．ディレクトリ内を開くためには読み込みだけで無く実行権限も付与する必要があります．

二つ目の注意点はエクスプローラー内にある`ホーム`，`デスクトップ`は使えないので`他の場所`からファイルを開く必要があることです．`他の場所`を選択してから現れる`コンピュータ`から，`home`→`kali`を選択してユーザー`kali`のホームディレクトリ`/home/kali` を開き，そこから`filter.ef`があるディレクトリを開いていきます．

[SparkFun Qwiic Python package]: https://learn.sparkfun.com/tutorials/sparkfun-auto-phat-hookup-guide/all#software-configuration
[Auto pHATのデモスクリプト]: https://learn.sparkfun.com/tutorials/sparkfun-auto-phat-hookup-guide/all#python-package-examples
[JSON]: https://ja.wikipedia.org/wiki/JavaScript_Object_Notation

## 3. 各デバイスのI2Cアドレス

* Qwiic Quad Relay (pseudo device consists of ATtiny84): 0x6d
* Qwiic Button: 0x6f
* Auto pHAT Servo Controller (PCA9685): 0x40
* Auto pHAT Motor Driver (PSoC4245 and DRV8835): 0x5d
* Auto pHAT Encoder Reader (pseudo device consists of ATtiny84): 0x73
* Auto pHAT 9-DoF IMU (ICM20948): 0x69

### 3.1 各デバイスのI2Cアドレスの求め方
デバイスのアドレスは，デバイスを接続した場合と切り離した場合で `i2cdetect` を使ってアドレス一覧を調べることで見つけることができます．

以下の例ではQwiic Buttonを切り離した場合（上）と接続した場合（下）で `i2cdetect` を実行しています．ここで `1` はRaspberry Piが持つ二つのI2Cバス(1と2)の内，バス1を指定しています． `-y` オプションはスキャン実行確認の問い合わせを抑止しています．
```
pi@raspberrypi:~ $ sudo i2cdetect -y 1
     0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
00:                         -- -- -- -- -- -- -- --
10: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
20: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
30: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
40: 40 -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
50: -- -- -- -- -- -- -- -- -- -- -- -- -- 5d -- --
60: -- -- -- -- -- -- -- -- -- 69 -- -- -- -- -- --
70: 70 -- -- 73 -- -- -- --
pi@raspberrypi:~ $ sudo i2cdetect -y 1
     0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
00:                         -- -- -- -- -- -- -- --
10: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
20: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
30: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
40: 40 -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
50: -- -- -- -- -- -- -- -- -- -- -- -- -- 5d -- --
60: -- -- -- -- -- -- -- -- -- 69 -- -- -- -- -- 6f
70: 70 -- -- 73 -- -- -- --
pi@raspberrypi:~ $
```

### 3.2 Raspberry Piでコマンドを用いて書き込み，読み込みを行う方法
Raspberry Pi OSのコマンド `i2cset` と `i2cget` を用いることで Python スクリプトなどを用いずともI2Cバスにデータを送ること、読み取ることができます．
書き込みの例（Qwiic Quad Relay の全リレーを ON にする）
```
pi@raspberrypi:~ $ i2cset -y 1 0x6d 0x0b
pi@raspberrypi:~ $
```
書き込みの例（Qwiic Quad Relay の全リレーを OFF にする）
```
pi@raspberrypi:~ $ i2cset -y 1 0x6d 0x0a
pi@raspberrypi:~ $
```
書き込みの例（Qwiic Quad Relay のリレー1を ON/OFF の状態を反転する）
```
pi@raspberrypi:~ $ i2cset -y 1 0x6d 0x01
pi@raspberrypi:~ $
```
読み込みの例（Qwiic Button のステータスを読み取る．戻り値の3ビット目がボタンのステータス．デバイスのアドレス0x6fの後の0x03はデータアドレス．詳細はi2cgetのマニュアルと[qwiic_button.py](https://github.com/sparkfun/Qwiic_Button_Py/blob/main/qwiic_button.py#:~:text=self.is_pressed%20%3D%20int(button_status)%20%26%20~(0xFB))を参照してください．）
```
pi@raspberrypi:~ $ i2cget -y 1 0x6f 0x03
0x03
```
