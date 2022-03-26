import sys
import os
import pathlib
import unittest
import asyncio

FILE = pathlib.Path(__file__).absolute()
HERE = FILE.parent
sys.path.append(str(HERE.parent / 'src'))


class TestLanguageServer(unittest.IsolatedAsyncioTestCase):

    async def test_pyls(self):
        from vicode.lsp import client
        from vicode.lsp import protocol

        lsp = client.Client.from_filetype('python')

        def on_diagnostics(params):
            publishDiagnostic_future.set_result(params)
        lsp.callbacks[client.NotificationTypes.diagnostics] = on_diagnostics

        publishDiagnostic_future = asyncio.Future()

        # launch
        await lsp.launch(asyncio.get_running_loop())

        # initialize
        response = await lsp.request_initialize(protocol.InitializeParams(
            processId=os.getpid(),
            capabilities=protocol.ClientCapabilities(),
        ))
        self.assertTrue('capabilities' in response)

        # initialized
        lsp.notify_initialized(protocol.InitializedParams())

        # open
        uri = FILE
        lsp.notify_textDocument_didOpen(protocol.DidOpenTextDocumentParams(
            textDocument=protocol.TextDocumentItem(
                uri=str(uri),
                languageId='python',
                version=1,
                text=uri.read_text()
            )
        ))

        # diagnostics
        diagnostic = await publishDiagnostic_future
        self.assertIsNotNone(diagnostic)

        # shutdown
        await lsp.request_shutdown()
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
