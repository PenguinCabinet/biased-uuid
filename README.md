# biased-uuid
<img width="960" height="516" alt="スクリーンショット 2026-07-12 170131" src="https://github.com/user-attachments/assets/6c53df82-370e-4e16-9008-5376573ba4ca" />

線形合同法 (LCG) の出力から、意図的に偏った RFC 9562 UUIDv4 を返すCloudflare Worker です。偏ったUUIDが欲しい時にお使いください。暗号学的に安全ではなく、実用の識別子には使えません。

## Usage

### 8bitの線形合同法×16
8bitの線形合同法×16で作ったUUIDを取得できます。
```
curl biased-uuid.penguincabinet.workers.dev/8
```
[もしくは直接アクセス](https://biased-uuid.penguincabinet.workers.dev/8)
### 16bitの線形合同法×8
16bitの線形合同法×8で作ったUUIDを取得できます。
```
curl biased-uuid.penguincabinet.workers.dev
```
```
curl biased-uuid.penguincabinet.workers.dev/16
```
[もしくは直接アクセス](https://biased-uuid.penguincabinet.workers.dev/16)
### 32bitの線形合同法×4
32bitの線形合同法×4で作ったUUIDを取得できます。
```
curl biased-uuid.penguincabinet.workers.dev/32
```
[もしくは直接アクセス](https://biased-uuid.penguincabinet.workers.dev/32)


## dev

```sh
uv run pywrangler dev
curl http://localhost:8787/
curl http://localhost:8787/8
curl http://localhost:8787/16
curl http://localhost:8787/32
```

レスポンスは改行付きの UUID です。`GET` と `HEAD` のみを受け付け、キャッシュを禁止します。デプロイは次のコマンドです。

```sh
uv run pywrangler deploy
```

テスト:

```sh
python -m unittest discover -s tests
```

`/8` は16個の8ビット LCG 出力を連結して生成します。`/` と `/16` は8個の16ビット LCG 出力を連結し、`/32` は4個の32ビット LCG 出力を連結して生成します。存在しないパスには404を返します。

Python の `uuid.UUID(..., version=4)` で versionを4、variantをRFC準拠に強制しているため、正しい形式のUUIDv4になります。
