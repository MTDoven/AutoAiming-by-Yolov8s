# AutoAiming-by-Yolov8s
This program is an implement of yolov8, which can help you aim in a shooting game. The biggest advantage is that it can run **extremely fast (average 98.4fps on RTX3060)**. Thanks to its high performance, similar framework may be applied to other fields, such as the tracking of high-speed moving objects.

## Requirement
Generally speaking, **Python>=3.7 and PyTorch>=1.7** is enough. But I use **Python==3.9 and PyTorch==2.1.0** (Originally I wanted to use torch.compile(model) to accelerate the program. But it has not supported on Windows yet). Other requirements are as follows:

        pip install ultralytics
        pip install pyautogui
        pip install keyboard
        pip install mss

## Usage
For using the pretrained model in a shooting game such as PUBG, you can just **enter the project folder** and run 
``python Inference.py``. By default, **pressing the "ALT" key** to start inference and auto-aiming.

You can check the **"Configure.py"**. I believe you can understand and adjust those few lines of code.

For a quick change for other usage. You can only pay attention to **"shotscreen" function in Inference.py** and **"callback" function in Callback.py** . They are the input and output of the yolo model.

## Train
For training, I suggest you check the official website:
[Ultralytics YOLOv8 documentation](https://docs.ultralytics.com/). They give more detailed steps for model training. Although I give some convenient tools here, I can't guarantee that each of them will work correctly on every computer.

Dataset structure:

        ├─DataSet
        │  ├─Annotations
        │  │  ├─XXXXXX.xml
        │  ├─images
        │  │  ├─XXXXXX.jpg
        │  ├─ImageSets
        │  │  ├─test.txt
        │  │  ├─train.txt
        │  │  ├─trainval.txt
        │  │  ├─val.txt
        │  ├─labels
        │  │  └─XXXXXX.txt
        │  ├─test.txt
        │  ├─train.txt
        │  ├─val.txt
        │  └─mydata.yaml
        └─TrainTool

1. Put your annotation in the folder annotation with format of ".xml". Put your image in the folder images. And ensure that the file name of the image and the label correspond to each other.
2. Run ``python HandleName.py`` under TrainTool folder, which will change the names to "001803.jpg" for example. Then run ``python SplitDataSet.py`` to generate four files in "DataSet/ImageSets/". And run ``python XML2TXT.py`` to transform ".xml" to ".txt" in the path of "/DataSet/labels/"
3. Write a file **"DataSet/mydata.yaml"** in this way:

        # It is recommended to write an absolute path
        train: xxx/DataSet/train.txt
        val: xxx/DataSet/val.txt
        test: xxx/DataSet/test.txt
        # number of classes
        nc: 2
        # class names
        names: ['person',"self"]
4. The final step, you can run ``yolo detect train data=../DataSet/mydata.yaml model=yolov8s.yaml epochs=300 imgsz=640 batch=-1``. Then pick your model in the path of "TrainTool/run/detect/train/". 
5. To Compiling C code into a "dll" requires only one line of code ``gcc -fPIC CFunctions.cpp -shared -o CFunctions.dll``. Try not to include a head of "c++", it will cause an odd problem I have not solved yet.

Thanks to Ultralytics that has packaged the various codes and parameters required in training, making the training process automatic. If you want to modify the specific training parameters, you can check the official website: [Ultralytics YOLOv8 documentation for training](https://docs.ultralytics.com/modes/train/)

## Notes
1. Use "mss" module to shot screen can be much more faster than "pyautogui" and much more easier than "win32api".  
2. I have overwrite some preprocess and postprecess part in the original code of ultralytics. Because they spend too much time to check the format of the picture inputed and to draw a beautiful picture to render the result. As a repeating task, we can cut down some process to make the program faster.
3. Instead of passing the processed data back into Python, which would take a lot of time. I called C's dynamic link library directly and passed in a pointer to the current data, and let the Windows API help us implement simulated mouse input.
4. I used multithreading to make the inference and the screenshot of the next graph run at the same time, resulting in faster speed.
