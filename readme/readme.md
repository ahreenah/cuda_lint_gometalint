Linter for CudaLint plugin.
Supports Go lexer.

It uses gometa tool:
- on Linux/macOS: install "gometa" package like this
  + install Go from https://golang.org/dl/
  + install gometalinter
    ```
    go get github.com/alecthomas/gometalinter
    gometalinter --install --update
    ```
- on Windows: download and install gometa from GitHub

Ported from SublimeLinter-contrib-gometalinter by Medvosa
