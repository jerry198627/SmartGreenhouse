import time
import picamera
import numpy as np
import matplotlib.pyplot as plt
import pickle
#ax = plt.figure()
#plt.show()
while True:
    with picamera.PiCamera() as camera:
        camera.resolution = (320, 240)
        camera.framerate = 24
        time.sleep(0.5)
        output = np.empty((240, 320, 3), dtype=np.uint8)
        camera.capture(output, 'rgb')
        
    print(f"out: {output}")
    output = pickle.dumps(output)
    print(f"Pickeled: {len(output)}")
    final = pickle.loads(output)
    print(f"Unpickled: {final}")
    ax = plt.imshow(final)
    plt.draw()
    plt.pause(0.00001)
    plt.clf()