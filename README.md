# vicode
vscode style vi powered by [ptk](https://python-prompt-toolkit.readthedocs.io/en/master/index.html).

## layout

```
+-------+------+
|sidebar|editor|
|       +------+
|       |panel |
+-------+------+
|command       |
+--------------+
```

## keyboard shortcut

- `c-w h`: focus sidebar
- `c-w j`: forus panel
- `c-w k`: focus editor
- `c-w l`: focus editor
- `m-h`: focus prev tab
- `m-l`: focus next tab

## TODO:

* [ ] lexer: syntax highlight
* [x] editor: tab
* [ ] editor: lineno
* [ ] editor: sign
* [x] panel: tab
* [x] panel: logger
* [x] sidebar: tab
* [ ] command: completion. :e
* [x] lsp: client
* [ ] lsp: diagnostics
* [ ] lsp: completion
* [ ] lsp: jump defnition
* [ ] lsp: hover
* [ ] side: fileselector
* [ ] side: bufferselector
* [ ] side: test runner
* [ ] dap: launcher
* [ ] dap: breakpoint
* [ ] dap: variable list
* [ ] dap: call stack
