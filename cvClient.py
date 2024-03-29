import json

# Asyncio (for concurrency)
import asyncio

# Websockets (for communication with the server)
from websockets.sync.client import connect, ClientConnection # type: ignore
from websockets.exceptions import ConnectionClosedError # type: ignore
from websockets.typing import Data # type: ignore

# Game state
from gameState import GameState

# Server messages
from serverMessage import *

# Restore the ability to use Ctrl + C within asyncio
import signal
signal.signal(signal.SIGINT, signal.SIG_DFL)

# Terminal colors for formatting output text
from terminalColors import *

from cv_locater import capture_loc, clean
from cv_arena import wall_correction

# Get the connect URL from the config.json file
def getConnectURL() -> str:

	# Read the configuration file
	with open('../config.json', 'r', encoding='UTF-8') as configFile:
		config = json.load(configFile)

	# Return the websocket connect address
	return f'ws://{config["ServerIP"]}:{config["WebSocketPort"]}'

class PacbotClient:
	'''
	Sample implementation of a websocket client to communicate with the
	Pacbot game server, using asyncio.
	'''

	def __init__(self, connectURL: str) -> None:
		'''
		Construct a new Pacbot client object
		'''

		# Connection URL (starts with ws://)
		self.connectURL: str = connectURL

		# Private variable to store whether the socket is open
		self._socketOpen: bool = False

		# Connection object to communicate with the server
		self.connection: ClientConnection

		# Game state object to store the game information
		self.state: GameState = GameState()
    
	async def run(self) -> None:
		'''
		Connect to the server, then run
		'''

		# Connect to the websocket server
		await self.connect()

		try: # Try receiving messages indefinitely
			if self._socketOpen:
				await asyncio.gather(
					self.receiveLoop(),
                    self.cvLoop()
				)
		finally: # Disconnect once the connection is over
			await self.disconnect()

	async def connect(self) -> None:
		'''
		Connect to the websocket server
		'''

		# Connect to the specified URL
		try:
			self.connection = connect(self.connectURL)
			self._socketOpen = True
			self.state.setConnectionStatus(True)

		# If the connection is refused, log and return
		except ConnectionRefusedError:
			print(
				f'{RED}Websocket connection refused [{self.connectURL}]\n'
				f'Are the address and port correct, and is the '
				f'server running?{NORMAL}'
			)
			return

	async def disconnect(self) -> None:
		'''
		Disconnect from the websocket server
		'''

		# Close the connection
		if self._socketOpen:
			self.connection.close()
		self._socketOpen = False
		self.state.setConnectionStatus(False)

	# Return whether the connection is open
	def isOpen(self) -> bool:
		'''
		Check whether the connection is open (unused)
		'''
		return self._socketOpen

	async def receiveLoop(self) -> None:
		'''
		Receive loop for capturing messages from the server
		'''

		# Receive values as long as the connection is open
		while self.isOpen():

			# Try to receive messages (and skip to except in case of an error)
			try:

				# Receive a message from the connection
				message: Data = self.connection.recv()

				# Convert the message to bytes, if necessary
				messageBytes: bytes
				if isinstance(message, bytes):
					messageBytes = message # type: ignore
				else:
					messageBytes = message.encode('ascii') # type: ignore

				# Update the state, given this message from the server
				self.state.update(messageBytes)

				# Write a response back to the server if necessary
				if self.state.writeServerBuf and self.state.writeServerBuf[0].tick():
					response: bytes = self.state.writeServerBuf.popleft().getBytes()
					self.connection.send(response)

				# Free the event loop to allow another decision
				await asyncio.sleep(0)

			# Break once the connection is closed
			except ConnectionClosedError:
				print('Connection lost...')
				self.state.setConnectionStatus(False)
				break

	async def cvLoop(self) -> None:
		while self.state.isConnected():

			# If the current messages haven't been sent out yet, skip this iteration
			if len(self.state.writeServerBuf):
				await asyncio.sleep(0)
				continue

			# Write back to the server, as a test (move right)
			pac_pos = capture_loc()
			print("Original: ",pac_pos)
			pac_pos = wall_correction(pac_pos)
			print("Wall corrected: ",pac_pos)

			if (pac_pos[0] > 0 and pac_pos[1] > 0):
				cv_output = [b'x',(pac_pos[1]).to_bytes(),(pac_pos[0]).to_bytes()]
				self.state.writeServerBuf.append(
                ServerMessage(b''.join(cv_output),1)
				)
			

			# Free up the event loop
			await asyncio.sleep(0)

# Main function
async def main():

	# Get the URL to connect to
	connectURL = getConnectURL()
	client = PacbotClient(connectURL)
	await client.run()

	# Once the connection is closed, end the event loop
	loop = asyncio.get_event_loop()
	loop.stop()
	clean()

if __name__ == '__main__':

	# Run the event loop forever
	loop = asyncio.get_event_loop()
	loop.create_task(main())
	loop.run_forever()