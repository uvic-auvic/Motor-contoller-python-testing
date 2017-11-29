import motor_control, time
import numpy as np

motor_control.rev_up(40, 80, 0.02)

recorded_rpm = []

for i in range(500):
	recorded_rpm.append(motor_control.get_rpm())
	time.sleep(1)

print("Mean: " + str(np.mean(recorded_rpm)))
print("Stddev: " + str(np.std(recorded_rpm)))
print("Min: " + str(np.min(recorded_rpm)))
print("Max: " + str(np.max(recorded_rpm)))
	
motor_control.stop()