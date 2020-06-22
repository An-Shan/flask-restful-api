from keras.preprocessing.image import  image
from numpy import expand_dims
import numpy as np
import matplotlib.pyplot as plt

product_list = ['雙肩後背包','水桶包','旅行包',
  '隨身腰包','旅行箱','郵差包',
  '馬鞍包','劍橋包','睡袋','托特包']

def find_image(test_model, img_path = 'Test_data/01.jpg'):
    try:
        img = image.load_img(img_path,target_size=(224,224))
        img = np.asarray(img)
        img = np.expand_dims(img, axis=0)

        plt.imshow(img[0])
        output = list(test_model.predict(img)[0])
        print(output)
        
        maxindex = output.index(max(output))
        return {'text' : '您是否是要查詢:' + str(product_list[maxindex])}

    except Exception as e:
        return {'text':str(e).split(':')[0]}