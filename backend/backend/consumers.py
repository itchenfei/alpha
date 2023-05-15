import asyncio
import paramiko
from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer


class SSHConsumer(AsyncWebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.loop = asyncio.get_event_loop()
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.channel = None
        self.transport = None

    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        if self.channel is not None:
            self.channel.close()
        if self.transport is not None:
            self.transport.close()

    async def receive(self, text_data):
        if self.channel is None:
            username, password, host, port = text_data.split(',')
            await self.loop.run_in_executor(None, self.ssh.connect, host, port, username, password)
            self.transport = self.ssh.get_transport()
            self.channel = self.transport.open_session()
            self.channel.get_pty()
            self.channel.invoke_shell()
            self.loop.create_task(self.send_ssh_output())

    async def send_ssh_output(self):
        while True:
            if self.channel.recv_ready():
                output = self.channel.recv(1024)
                await self.send(output)
            else:
                await asyncio.sleep(0.1)
