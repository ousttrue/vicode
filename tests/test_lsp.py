import sys
import pathlib
import unittest
import asyncio

HERE = pathlib.Path(__file__).absolute().parent
sys.path.append(str(HERE.parent / 'src'))


class TestLanguageServer(unittest.IsolatedAsyncioTestCase):

    async def test_pyls(self):
        from vicode.lsp import language_server

        server = await language_server.popen(asyncio.get_event_loop())
        self.assertIsNotNone(server)

        response = await server.requestInitialize()
        self.assertIsNotNone(response)


if __name__ == '__main__':
    unittest.main()
