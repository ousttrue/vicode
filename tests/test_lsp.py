import sys
import os
import pathlib
import unittest
import asyncio

HERE = pathlib.Path(__file__).absolute().parent
sys.path.append(str(HERE.parent / 'src'))


class TestLanguageServer(unittest.IsolatedAsyncioTestCase):

    async def test_pyls(self):
        from vicode.lsp import language_server
        from vicode.lsp.protocol import InitializeParams, ClientCapabilities

        server = await language_server.popen(asyncio.get_event_loop())
        self.assertIsNotNone(server)

        response = await server.requestInitialize(InitializeParams(
            processId=os.getpid(),
            capabilities=ClientCapabilities(),
        ))
        self.assertIsNotNone(response)


if __name__ == '__main__':
    unittest.main()
