import tkinter as tk
from threading import Thread, Event
from time import sleep
import asyncio
from bleak import BleakScanner, BleakClient
import struct
import tkinter.font as tkFont
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time


from Save_GUI import Save_Data_GUI

ACCEL_VALUES = []
TIME_VALUES = []

class MainGUI:
	def __init__(self, e, async_loop):
		light_gray = '#404040'
		bright_orange = '#ff8303'
		dark_orange = '#ff8303'#'#a35709'
		slate = '#1b1a17'

		self.root = tk.Tk()
		self.root.geometry('1400x800')
		self.root.title("Testing")
		self.root.configure(bg=slate)

		message_font_style = tkFont.Font(size=30)

		self.e = e

		self.async_loop = async_loop

		self.collecting_data = False

		self.data = DataUpdate()

		self.mass_entered = 0
		self.max_accel = 0
		self.max_vel = 0
		self.max_force = 0
		self.lift_type = ''


		### FRAMES
		self.title_frame = tk.Frame(self.root)
		self.title_frame.grid(column=0, row=0)

		self.middle_frame = tk.Frame(self.root, bg=slate)
		self.middle_frame.grid(column=0, row=1)

		self.button_frame = tk.Frame(self.middle_frame)
		self.button_frame.grid(column=0, row=1)

		self.graph_frame = tk.Frame(self.middle_frame)
		self.graph_frame.grid(column=0, row=0)

		self.datainput_frame = tk.Frame(self.middle_frame, bg=light_gray)
		self.datainput_frame.grid(column=1, row=0)

		self.datainput_label_frame = tk.Frame(self.datainput_frame, bg=light_gray)
		self.datainput_label_frame.grid(column=0, row=0)

		self.datainput_ouput_frame = tk.Frame(self.datainput_frame, bg=light_gray)
		self.datainput_ouput_frame.grid(column=1, row=0)

		### MESSAGES
		self.title_message = tk.Message(self.title_frame, font=message_font_style)
		self.title_message.grid(column=0, row=0)
		self.title_message.configure(text='Force Production Tracker', bg=slate, fg=bright_orange, width=800)

		self.datainput_label = tk.Label(self.datainput_label_frame, text='Enter Mass Used (lbs):')
		self.datainput_label.grid(column=0, row=0)
		self.datainput_label.configure(fg=dark_orange, bg=light_gray, anchor='w', width=20)

		self.mass_label = tk.Label(self.datainput_label_frame, text='Mass (lbs):')
		self.mass_label.grid(column=0, row=1)
		self.mass_label.configure(fg=dark_orange, bg=light_gray, anchor='w', width=20)

		self.acceleration_label = tk.Label(self.datainput_label_frame, text='Max Acceleration (g):')
		self.acceleration_label.grid(column=0, row=2)
		self.acceleration_label.configure(fg=dark_orange, bg=light_gray, anchor='w', width=20)

		self.maxvel_label = tk.Label(self.datainput_label_frame, text='Max Velocity (m/s):')
		self.maxvel_label.grid(column=0, row=3)
		self.maxvel_label.configure(fg=dark_orange, bg=light_gray, anchor='w', width=20)

		self.maxforce_label = tk.Label(self.datainput_label_frame, text='Max Force (N):')
		self.maxforce_label.grid(column=0, row=4)
		self.maxforce_label.configure(fg=dark_orange, bg=light_gray, anchor='w', width=20)

		self.mass_output = tk.Label(self.datainput_ouput_frame, text=str(self.mass_entered))
		self.mass_output.grid(column=0, row=1)
		self.mass_output.configure(fg=dark_orange, bg=light_gray, anchor='e', width=6)

		self.acceleration_output = tk.Label(self.datainput_ouput_frame, text=str(self.max_accel))
		self.acceleration_output.grid(column=0, row=2)
		self.acceleration_output.configure(fg=dark_orange, bg=light_gray, anchor='e', width=6)

		self.velocity_output = tk.Label(self.datainput_ouput_frame, text=str(self.max_vel))
		self.velocity_output.grid(column=0, row=3)
		self.velocity_output.configure(fg=dark_orange, bg=light_gray, anchor='e', width=6)

		self.force_output = tk.Label(self.datainput_ouput_frame, text=str(self.max_force))
		self.force_output.grid(column=0, row=4)
		self.force_output.configure(fg=dark_orange, bg=light_gray, anchor='e', width=6)
		
		### MASS ENTRY
		#self.mass_entry_frame = tk.Frame(self.datainput_frame)
		#self.mass_entry_frame.grid(column=0, row=0)

		self.mass_entry = tk.Entry(self.datainput_ouput_frame)
		self.mass_entry.grid(column=0, row=0)
		self.mass_entry.configure(width=8)
		self.mass_entry.bind('<Return>', self.submit_mass)


		### BUTTONS
		self.connect_button = tk.Button(self.button_frame, text='Connect', command=lambda:self.do_tasks())
		self.connect_button.grid(column=0, row=0)
		self.connect_button.configure(fg=bright_orange, bg=slate, relief='raised', height=2, width=10)

		self.start_stop_button = tk.Button(self.button_frame, text='Start/Stop', command=self.click_start_stop)
		self.start_stop_button.grid(column=1, row=0)
		self.start_stop_button.configure(fg=bright_orange, bg=slate, relief='raised', height=2, width=10, state=tk.DISABLED)

		self.reset_button = tk.Button(self.button_frame, text='Reset Graph', command=self.click_reset)
		self.reset_button.grid(column=2, row=0)
		self.reset_button.configure(fg=bright_orange, bg=slate, relief='raised', height=2, width=10, state=tk.DISABLED)

		self.save_button = tk.Button(self.button_frame, text='Save', command=self.click_save)
		self.save_button.grid(column=3, row=0)
		self.save_button.configure(fg=bright_orange, bg=slate, relief='raised', height=2, width=10)

		self.open_button = tk.Button(self.button_frame, text='Open', command=self.click_open)
		self.open_button.grid(column=4, row=0)
		self.open_button.configure(fg=bright_orange, bg=slate, relief='raised', height=2, width=10)

		self.quit_button = tk.Button(self.button_frame, text='Quit', command=self.click_quit)
		self.quit_button.grid(column=5, row=0)
		self.quit_button.configure(fg=bright_orange, bg=slate, relief='raised', height=2, width=10)

		### GRAPH
		self.plot_canvas = FigureCanvasTkAgg(self.data.fig, master=self.graph_frame)
		self.plot_canvas.get_tk_widget().grid(column=0, row=2)
		self.plot_canvas.get_tk_widget().configure(bg=slate)

		ani = animation.FuncAnimation(self.data.fig, self.data.plot_data, interval=125)



		self.root.mainloop()

	def do_tasks(self):
		self.connect_button.configure(state=tk.DISABLED)
		
		print('Starting collection thread, please wait 10 seconds for calibration...')
		self.t = Thread(target=self._asyncio_thread).start()
		for x in range(10, 0, -1):
			print(x)
			time.sleep(1)

		self.start_stop_button.configure(state=tk.NORMAL)
		self.reset_button.configure(state=tk.NORMAL)

	def _asyncio_thread(self):
		self.async_loop.create_task(self.data.get_data(self.e))
		self.async_loop.run_forever()
		#self.async_loop.run_until_complete(self.data.get_data(self.e))

	def click_start_stop(self):
		if self.e.is_set():
			self.e.clear()
			print('Stopped recording...')
		else:
			if len(self.data.tot_y_data) > 0:
				self.click_reset()

			self.e.set()
			print('Recording...')

	def click_reset(self):
		self.data.reset_data()

	def click_save(self):
		xdata, ydata = self.data.get_data_tosave()
		Save_Data_GUI(xdata, ydata, self.mass_entered, self.lift_type)

	def click_open(self):
		pass

	def submit_mass(self, event=None):
		try:
			entry = int(self.mass_entry.get())
		except:
			return
		self.mass_entered = entry
		self.mass_output.configure(text=self.mass_entry.get())

	def click_quit(self):
		self.data._quit()
		self.root.quit()
		self.root.destroy()
		self.async_loop.stop()


class DataUpdate():
	def __init__(self):
		self.ble_address = "92:9E:CA:30:D6:48"#92:9E:CA:30:D6:E0"
		self.accel_service = "00001101-0000-1000-8000-00805f9b34fb"
		self.characteristic_uuid = "00002101-0000-1000-8000-00805f9b34fb"

		self.start_time = None

		light_gray = '#404040'
		bright_orange = '#ff8303'
		dark_orange = '#a35709'
		slate = '#1b1a17'

		self.axlims = [0, 5]
		self.vxlims = [0, 5]
		self.aylims = [-2, 2]
		self.vylims = [-10, 10]

		self.tot_x_data = []
		self.tot_y_data = []
		self.vel_y_data = []
		self.vel_x_data = []

		#plt.style.use('dark_background')
		self.fig, (self.ax_accel, self.ax_vel) = plt.subplots(1, 2, figsize=(6,3))
		self.fig.patch.set_facecolor(slate)
		self.ax_accel.set_facecolor(slate)
		self.ax_vel.set_facecolor(slate)
		self.ax_accel.set_title('Acceleration', color=bright_orange)
		self.ax_vel.set_title('Velocity', color=bright_orange)
		self.ax_accel.set_ylim(self.aylims[0], self.aylims[1])
		self.ax_accel.set_xlim(self.axlims[0], self.axlims[1])
		self.ax_vel.set_ylim(self.vylims[0], self.vylims[1])
		self.ax_vel.set_xlim(self.vxlims[0], self.vxlims[1])
		self.ax_accel.tick_params(axis='x', colors=bright_orange)
		self.ax_accel.tick_params(axis='y', colors=bright_orange)
		self.ax_vel.tick_params(axis='x', colors=bright_orange)
		self.ax_vel.tick_params(axis='y', colors=bright_orange)

		for spine in self.ax_accel.spines:
			self.ax_accel.spines[spine].set_color(bright_orange)
			self.ax_vel.spines[spine].set_color(bright_orange)
		self.accel_line, = self.ax_accel.plot([], [], color=bright_orange, marker=',')
		self.vel_line, = self.ax_vel.plot([], [], color=bright_orange, marker=',')
		self.fig.tight_layout()
		
	def plot_data(self, i):
		self.accel_line.set_data(self.tot_x_data, self.tot_y_data)

		if len(self.tot_y_data) > 0:
			#set accel x lims if longer
			if self.tot_x_data[-1] > self.axlims[1]:
				self.axlims[1] = self.tot_x_data[-1]
				self.ax_accel.set_xlim(*self.axlims)

			#set accel y lims if higher
			if self.tot_y_data[-1] > self.aylims[1]:
				self.aylims[1] = self.tot_y_data[-1]
				self.ax_accel.set_ylim(*self.aylims)

			#set accel y lims if lower 
			if self.tot_y_data[-1] < self.aylims[0]:
				self.aylims[0] = self.tot_y_data[-1]
				self.ax_accel.set_ylim(*self.aylims)

			if len(self.tot_y_data) > 2:
				
				self.vel_y_data.append((self.tot_y_data[-2] - self.tot_y_data[-1]) / (self.tot_x_data[-2] - self.tot_x_data[-1]))
				self.vel_x_data.append(self.tot_x_data[-1])
				self.vel_line.set_data(self.vel_x_data, self.vel_y_data)

				#set vel x lims if longer
				if self.vel_x_data[-1] > self.vxlims[1]:
					self.vxlims[1] = self.vel_x_data[-1]
					self.ax_vel.set_xlim(*self.vxlims)

				if self.vel_y_data[-1] > self.vylims[1]:
					self.vylims[1] = self.vel_y_data[-1]
					self.ax_vel.set_ylim(*self.vylims)

				if self.vel_y_data[-1] < self.vylims[0]:
					self.vylims[0] = self.vel_y_data[-1]
					self.ax_vel.set_ylim(*self.vylims)


	async def get_data(self, e):
		async with BleakClient(self.ble_address) as client:
			print('Beginning data collection...')
			while True:
				read_value = await client.read_gatt_char(self.characteristic_uuid)
				if e.is_set():
					if not self.start_time:
						self.start_time = time.time()
					read_value = struct.unpack('f', read_value)
					new_time = time.time()
					self.tot_y_data.append(read_value[0]) #read_value is a tuple of 1?
					self.tot_x_data.append(new_time - self.start_time)
					print(new_time - self.start_time)

	def reset_data(self):
		self.tot_x_data = []
		self.tot_y_data = []
		self.vel_x_data = []
		self.vel_y_data = []
		self.axlims = [0, 5]
		self.vxlims = [0, 5]
		self.aylims = [-2, 2]
		self.vylims = [-10, 10]
		self.ax_accel.set_xlim(*self.axlims)
		self.ax_vel.set_xlim(*self.vxlims)
		self.ax_accel.set_ylim(*self.aylims)
		self.ax_vel.set_ylim(*self.vylims)
		self.start_time = None
		self.vel_line.set_data(self.vel_x_data, self.vel_y_data)

	def get_data_tosave(self):
		return (self.tot_x_data, self.tot_y_data)

	def _quit(self):
		pass




##SEE IF WE CAN MAKE IT STAY CONNETED TO ADDRESS SO IT CAN RESUME READING FASTER
##ONLY STOP SAVING INFO NOT STOP READING? OR DONT CALL AWAIT READ_GATT_CHAR?

def main(async_loop):
	event = Event()
	gui = MainGUI(event, async_loop)

if __name__ == '__main__':
	async_loop = asyncio.get_event_loop()
	main(async_loop)


# def modify_variable(var):
#     while True:
#         for i in range(len(var)):
#             var[i] += 1
#         if event.is_set():
#             break
#         sleep(.5)
#     print('Stop printing')


# my_var = [1, 2, 3]
# t = Thread(target=modify_variable, args=(my_var, ))
# t.start()
# while True:
#     try:
#         print(my_var)
#         sleep(1)
#     except KeyboardInterrupt:
#         event.set()
#         break
# t.join()
# print(my_var)