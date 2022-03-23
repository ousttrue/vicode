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

        client = await client.popen(asyncio.get_event_loop())
        self.assertIsNotNone(client)

        publishDiagnostic_future = asyncio.Future()

        def on_notify(params):
            publishDiagnostic_future.set_result(params)
        client.rpcDispatcher.on_notify(
            'textDocument/publishDiagnostics', on_notify)

        # initialize
        response = await client.request_initialize(protocol.InitializeParams(
            processId=os.getpid(),
            capabilities=protocol.ClientCapabilities(),
        ))
        self.assertTrue('capabilities' in response)

        # initialized
        client.notify_initialized(protocol.InitializedParams())

        # open
        uri = FILE
        client.notify_textDocument_didOpen(protocol.DidOpenTextDocumentParams(
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
        await client.request_shutdown()
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
