import asyncio
import monome
import rtmidi

midiout = rtmidi.MidiOut()

class HelloApp(monome.GridApp):
    def __init__(self):
        super().__init__()
        self.width = 16
        self.height = 8
        self.on_keys = [ [0]*self.height for i in range(self.width)]
        midiout.open_virtual_port("Monome CC Selector")

    def on_grid_ready(self):
        self.grid.led_all(0)
    
    def on_grid_key(self, x, y, s):
        if s is 1:
            if self.on_keys[x][y] is 1:
                self.on_keys[x][y] = 0
            else:
                self.on_keys[x][y] = 1
            self.grid.led_set(x, y, self.on_keys[x][y])
            midiout.send_message([0xB2, (self.width*y)+x, 127*self.on_keys[x][y]])

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    hello_app = HelloApp()

    print("running...")
    
    def serialosc_device_added(id, type, port):
        print('connecting to {} ({})'.format(id, type))
        asyncio.ensure_future(hello_app.grid.connect('127.0.0.1', port))

    serialosc = monome.SerialOsc()
    serialosc.device_added_event.add_handler(serialosc_device_added)

    loop.run_until_complete(serialosc.connect())

    loop.run_forever()
