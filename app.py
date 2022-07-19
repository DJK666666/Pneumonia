{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      " * Serving Flask app \"__main__\" (lazy loading)\n",
      " * Environment: production\n",
      "\u001b[31m   WARNING: This is a development server. Do not use it in a production deployment.\u001b[0m\n",
      "\u001b[2m   Use a production WSGI server instead.\u001b[0m\n",
      " * Debug mode: off\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      " * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)\n",
      "127.0.0.1 - - [19/Jul/2022 14:45:25] \"GET / HTTP/1.1\" 200 -\n"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "File Received\n",
      "IM-0001-0001.jpeg\n",
      "1/1 [==============================] - 0s 245ms/step\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "127.0.0.1 - - [19/Jul/2022 14:45:33] \"POST / HTTP/1.1\" 200 -\n"
     ]
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "File Received\n",
      "IM-0009-0001.jpeg\n",
      "1/1 [==============================] - 0s 142ms/step\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "127.0.0.1 - - [19/Jul/2022 14:46:41] \"POST / HTTP/1.1\" 200 -\n"
     ]
    }
   ],
   "source": [
    "from flask import Flask, render_template, request\n",
    "from werkzeug.utils import secure_filename\n",
    "from skimage import io\n",
    "from keras.models import load_model\n",
    "import cv2\n",
    "from PIL import Image #use PIL\n",
    "import numpy as np\n",
    "\n",
    "app = Flask(__name__)\n",
    "\n",
    "@app.route('/', methods=['GET', 'POST'])\n",
    "def upload_file():\n",
    "    if request.method == 'POST':\n",
    "        file = request.files['file']\n",
    "        print(\"File Received\")\n",
    "        filename = secure_filename(file.filename)\n",
    "        print(filename)\n",
    "        file.save(\"./static/\"+filename) #Heroku no need static\n",
    "        file = open(\"./static/\"+filename,\"r\") #Heroku no need static\n",
    "        model = load_model(\"Pneumonia\")\n",
    "        image = cv2.imread(\"./static/\"+filename)\n",
    "        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)\n",
    "        img = cv2.merge([gray,gray,gray])\n",
    "        img.resize((150,150,3))\n",
    "        img = np.asarray(img, dtype=\"float32\") #need to transfer to np to reshape\n",
    "        img = img.reshape(1, img.shape[0], img.shape[1], img.shape[2]) #rgb to reshape to 1,100,100,3\n",
    "        pred=model.predict(img)\n",
    "        return(render_template(\"index.html\", result=str(pred)))\n",
    "    else:\n",
    "        return(render_template(\"index.html\", result=\"WAITING\"))\n",
    "if __name__ == \"__main__\":\n",
    "    app.run()\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.9.12"
  },
  "vscode": {
   "interpreter": {
    "hash": "88279d2366fe020547cde40dd65aa0e3aa662a6ec1f3ca12d88834876c85e1a6"
   }
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}
