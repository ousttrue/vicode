# vicode
vscode style vi powered by [ptk](https://python-prompt-toolkit.readthedocs.io/en/master/index.html).
Developed with reference to [pyvim](https://github.com/prompt-toolkit/pyvim).

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

* [x] lexer: syntax highlight
* [x] editor: tab
* [x] editor: merge: lineno
* [ ] editor: merge: sign
* [x] editor: word completion
* [ ] editor: buffer search
* [x] panel: tab
* [x] panel: logger
* [x] sidebar: tab
* [x] command: e
* [ ] command: bd
* [ ] command: w
* [x] lsp: client
* [x] lsp: diagnostics jumplist
* [ ] lsp: diagnostics high light
* [ ] lsp: completion
* [ ] lsp: defnition(jump)
* [ ] lsp: hover
* [ ] sidebar: fileselector
* [ ] sidebar: bufferselector
* [ ] sidebar: test runner
* [ ] dap: launcher
* [ ] dap: merge: breakpoint
* [ ] dap: variable list
* [ ] dap: call stack

## References

* https://microsoft.github.io/language-server-protocol/
* https://microsoft.github.io/debug-adapter-protocol/
