# denki_cr

## [remote-i2c] package について
[remote-i2c] は Raspberry Pi の I2C を他の端末から制御することを可能とする python ライブラリパッケージです．
Raspberry Pi でサーバースクリプトを動かしておけば他の端末から Python スクリプトを用いて Raspberry Pi の I2C を操作できます．

remote-i2c のプロトコルは TCP を用いています．デフォルトの待受ポートは 5446 です。アドレスとデータをそのままバイナリのバイト列で送る至極簡単なプロトコルです。サーバーは受け取ったアドレス，データを I2C バスに送ります．
アドレスを指定してデータを読み込むことができます．

remote-i2c にはアクセス制限などの制御機構はありません．


[remote-i2c]: https://pypi.org/project/remote-i2c/

## [remote-i2c] package のインストール
### Rasberry Pi OS へのインストール

remote-i2c のインストール
```
sudo pip install remote-i2c
```

### Kali Linux へのインストール
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

## サンプルスクリプト

### `remote_i2c_server.py`
remote-i2c のドキュメントでも説明されているようにこのスクリプトを用いなくても以下のコマンでパッケージのデフォルトメソッドを実行することでサーバーとして動きます．
```
python -m remote_i2c
```

`remote_i2c_server.py` を用いる場合
```
python remote_i2c_server.py
```

### `remote_i2c_client.py`
remote-i2c のドキュメントに掲載してあるサンプルだとうまく動きません．これはスクリプト内で用いられているメソッド `bus.write_byte_data(addr, reg, value)` がSMBus用だからです．`remote_i2c_client.py` ではI2C用の書き込みメソッドは `bus.write_byte(addr, value)` を用いています．

サーバーの IP アドレスを `remote_i2c_host` に与えてください．

このスクリプトは Qwiic Quad Relay の全リレーの ON にし，1秒後に OFF にします．
この動作や他のデバイスに対応する場合はアドレスと書き込む値をデバイスの動作に合わせて変更してください．

スクリプトを一回だけ実行する方法
```
python remote_i2c_client.py
```

スクリプトを繰り返し実行したい場合は，スクリプト内で for などの繰り返し文を用いるか、以下のように Shell 言語の while コマンドを用います．
```
while : ; do python remote_i2c_client.py ; done
```

## 各デバイスのI2Cアドレス

* Qwiic Quad Relay (pseudo device consists of ATtiny84): 0x6d
* Qwiic Button: 0x64
* Auto pHAT Servo Controller (PCA9685): 0x40
* Auto pHAT Motor Driver (PSoC4245 and DRV8835): 0x5d
* Auto pHAT Encoder Reader (pseudo device consists of ATtiny84): 0x73
* Auto pHAT 9-DoF IMU (ICM20948): 0x69

## 各デバイスのI2Cアドレスの求め方
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

## Raspberry Piでコマンドを用いて書き込み，読み込みを行う方法
Raspberry Pi OSのコマンド `i2cset` と `i2cget` を用いることで Python スクリプトなどを用いずともI2Cバスにデータを送ること、読み取ることができます．
書き込みの例
```
i2pset -y 1 0x6d 0x0b
```
読み込みの例
```
i2cget -y 1 0x6d
```

