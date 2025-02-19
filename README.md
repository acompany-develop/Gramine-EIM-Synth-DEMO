# Gramine-EIM-Synth-DEMO

# 用語
| 用語 | 説明 |
| --- | --- |
| EIM | Enclaved ID Matching、Serverが2つのcsvを隔離領域でmatchingする|
| Synth | matching結果を用いてServerの隔離領域でCTGANを行い合成データのモデルを作成する |
| Gramine-EIM-Synth | 2つのClientがServerにcsvを送信し、ServerはEIM,Synthをして作成した合成データのモデルをClientに返送する 
| RA | Remote Attestation、SGXが安全であることを示し、安全なSSL通信を行うようにするプロトコル |

# ディレクトリ概要
```
.
├── README.md
├── demo_docker
│   ├── Dockerfile
│   ├── Makefile
│   ├── README.md
│   ├── bind
│   │   ├── Client0
│   │   │   └── settings_client.ini
│   │   ├── Client1
│   │   │   └── settings_client.ini
│   │   ├── data
│   │   │   ├── 100_a.csv
│   │   │   ├── 100_b.csv
│   │   │   └── make_dummy_data.py
│   │   └── output
│   └── docker-compose.yaml
├── docs
│   ├── README.md
│   ├── common_error.md
│   ├── data_in_out.md
│   ├── guarantee.md
│   ├── how_to_use.md
│   └── server_state.md
└── licenses
    ├── LICENSE_gramine
    └── LICENSE_linux-sgx
```
