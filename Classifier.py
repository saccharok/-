import torch
import cv2
import torchvision.transforms as transforms
from PIL import Image
import os
import Management
import time

model = torch.load("classifier.pth")
model.eval()
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)
cap = cv2.VideoCapture(0)

def get_class_number(imageRGB, check):
    if check == False:
        stop_classifier()
    predicted_class = -1
    pil_image = Image.fromarray(imageRGB)
    data_transform = transforms.Compose([
        transforms.Resize((350, 350)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5])
    ])
    transformed_image = data_transform(pil_image).unsqueeze(0)
    transformed_image = transformed_image.to(device)
    with torch.no_grad():
        output = model(transformed_image)
    _, predicted = torch.max(output, 1)
    predicted_class = predicted.item()
    return get_class_name(predicted_class)

def get_class_name(predicted_class):
    classes = ['call', 'dislike', 'fist', 'four', 'like', 'mute', 'ok', 'one', 'palm', 'peace', 'peace_inverted', 'rock', 'stop', 'stop_inverted', 'three', 'three2', 'two_up', 'two_up_inverted']
    if predicted_class < len(classes):
        return classes[predicted_class]
    else:
        return 'none'

def run_sorted(line):
    classes = ['call', 'dislike', 'fist', 'four', 'like', 'mute', 'ok', 'one', 'palm', 'peace', 'peace_inverted', 'rock', 'stop', 'stop_inverted', 'three', 'three2', 'two_up', 'two_up_inverted']
    for class_name in classes:
        new_path = os.path.join(line, class_name)
        os.mkdir(new_path)
    image_files = [f for f in os.listdir(line) if os.path.isfile(os.path.join(line, f))]
    for image_file in image_files:
        image_path = os.path.join(line, image_file)
        image = Image.open(image_path)
        
        predicted_class = -1
        data_transform = transforms.Compose([
            transforms.Resize((350, 350)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5])
        ])
        transformed_image = data_transform(image).unsqueeze(0)
        transformed_image = transformed_image.to(device)
        with torch.no_grad():
            output = model(transformed_image)
        _, predicted = torch.max(output, 1)
        predicted_class = predicted.item()
        predicted_class_name = get_class_name(predicted_class)
        new_image_path = os.path.join(line, predicted_class_name, image_file)
        os.rename(image_path, new_image_path)    

def stop_classifier():
    cap.release()

def run_classifier():    
    while True:
        check = True
        _, image = cap.read()
        if image is None:
            check = False
            stop_classifier()
            break
        image = cv2.flip(image, 1)
        imageRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        if cv2.waitKey(500) & 0xFF == 27:
            break
        gesture = get_class_number(imageRGB, check)
        Management.management(gesture)
        time.sleep(3)