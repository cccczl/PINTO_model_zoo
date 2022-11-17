import numpy as np
import math
import time
import sys
import cv2
try:
    from tflite_runtime.interpreter import Interpreter
except:
    from tensorflow.lite.python.interpreter import Interpreter

LABELS = [
'aeroplane','bicycle','bird','boat','bottle','bus','car','cat','chair','cow',
'diningtable','dog','horse','motorbike','person','pottedplant','sheep','sofa','train','tvmonitor']

if __name__ == '__main__':
    image = cv2.imread('dog.jpg')
    interpreter = Interpreter(model_path='03_integer_quantization/ssdlite_mobilenet_v2_voc_300_integer_quant_with_postprocess.tflite')
    try:
        interpreter.set_num_threads(4)
    except:
        print("WARNING: The installed PythonAPI of Tensorflow/Tensorflow Lite runtime does not support Multi-Thread processing.")
        print("WARNING: It works in single thread mode.")
        print("WARNING: If you want to use Multi-Thread to improve performance on aarch64/armv7l platforms, please refer to one of the below to implement a customized Tensorflow/Tensorflow Lite runtime.")
        print("https://github.com/PINTO0309/Tensorflow-bin.git")
        print("https://github.com/PINTO0309/TensorflowLite-bin.git")
    interpreter.allocate_tensors()
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

    start_time = time.perf_counter()

    image_height = image.shape[0]
    image_width  = image.shape[1]

    # Resize and normalize image for network input
    t3 = time.perf_counter()
    frame = cv2.resize(image, (300, 300))
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = np.expand_dims(frame, axis=0)
    frame = frame.astype(np.float32)
    cv2.normalize(frame, frame, -1, 1, cv2.NORM_MINMAX)
    t4 = time.perf_counter()
    print("resize and normalize time: ", t4 - t3)

    # run model
    t5 = time.perf_counter()
    interpreter.set_tensor(input_details[0]['index'], frame)
    interpreter.invoke()
    t6 = time.perf_counter()
    print("inference + postprocess time: ", t6 - t5)

    # get results
    boxes = interpreter.get_tensor(output_details[0]['index'])[0]
    classes = interpreter.get_tensor(output_details[1]['index'])[0]
    scores = interpreter.get_tensor(output_details[2]['index'])[0]
    count = interpreter.get_tensor(output_details[3]['index'])[0]

    for i, (box, classidx, score) in enumerate(zip(boxes, classes, scores)):
        probability = score
        if probability >= 0.6:
            if (
                math.isnan(box[0])
                or math.isnan(box[1])
                or math.isnan(box[2])
                or math.isnan(box[3])
            ):
                continue
            ymin = int(box[0] * image_height)
            xmin = int(box[1] * image_width)
            ymax = int(box[2] * image_height)
            xmax = int(box[3] * image_width)
            if ymin > ymax:
                continue
            if xmin > xmax:
                continue
            classnum = int(classidx)
            probability = score
            print('coordinates: ({}, {})-({}, {}). class: "{}". probability: {:.2f}'.format(xmin, ymin, xmax, ymax, classnum, probability))
            cv2.rectangle(image, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2)
            cv2.putText(image, '{}: {:.2f}'.format(LABELS[classnum],probability), (xmin, ymin - 5), cv2.FONT_HERSHEY_COMPLEX, 0.8, (0, 255, 0), 2)
        if i >= (count - 1):
            break

    stop_time = time.perf_counter()
    print("TOTAL time: ", stop_time - start_time)

    print(boxes, classes, scores, count)

    cv2.imwrite('result.jpg', cv2.cvtColor(image, cv2.COLOR_RGB2BGR))

