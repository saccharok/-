import torch
import torch.utils
import torch.utils.data
from torchvision.models import resnet18, ResNet18_Weights
from torchvision import transforms
from torchvision import datasets
import os
import matplotlib.pyplot as plt
import time

def get_dataset(dataDir, dataTransforms):
    image_datasets = {x: datasets.ImageFolder(os.path.join(dataDir, x), dataTransforms[x]) 
                      for x in ['train', 'test']}
    dataloaders = {x: torch.utils.data.DataLoader
                   (image_datasets[x], batch_size=4, shuffle=True, num_workers=8) 
                   for x in ['train', 'test']}
    dataset_sizes = {x: len(image_datasets[x]) for x in ['train', 'test']}
    classes = image_datasets['train'].classes
    return dataloaders["train"], dataloaders['test'], classes, dataset_sizes

if __name__ == '__main__':
    dataDir = os.path.join(os.path.abspath(os.curdir), "data\\")
    dataTransforms = {
        'train': transforms.Compose([
            transforms.ToTensor(),
            transforms.Normalize([0.5, 0.5, 0.5], [0.5, 0.5, 0.5])
        ]),
        'test': transforms.Compose([
            transforms.ToTensor(),
            transforms.Normalize([0.5, 0.5, 0.5], [0.5, 0.5, 0.5])
        ]),
    }
    
    trainloader, testloader, classes, dataset_sizes = get_dataset(dataDir, dataTransforms)

    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    resnet18_model = resnet18(weights=ResNet18_Weights.DEFAULT).to(device)
    resnet18_model.train()
    next(resnet18_model.parameters()).is_cuda

    criterion = torch.nn.CrossEntropyLoss()
    resnet18_optim = torch.optim.Adam(resnet18_model.parameters(),lr=0.001)

    start = time.time()
    num_epochs = 5
    print('Start training')
    for epoch in range(num_epochs):
        running_loss = 0.0
        for i, data in enumerate(trainloader):
            inputs, labels = data[0].to(device), data[1].to(device)
            resnet18_optim.zero_grad()
            outputs = resnet18_model(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            resnet18_optim.step()
            running_loss += loss.item()
            #print(i)
        epoch_loss = running_loss / len(trainloader)
        print(f'Epoch: {epoch + 1}, Loss: {epoch_loss:.4f}')
        #running_loss = 0.0
        
    end = time.time()
    print(f"Total time: {end - start} sec")
    PATH =os.path.join(os.path.abspath(os.curdir), "classifier.pth")
    torch.save(resnet18_model, PATH)

    correct = 0
    total = 0
    correct_predictions = {class_name: 0 for class_name in classes}
    total_samples = {class_name: 0 for class_name in classes}
    with torch.no_grad():
        for data in testloader:
            images, labels = data
            images, labels = images.to(device), labels.to(device)
            outputs = resnet18_model(images)
            _, predicted = torch.max(outputs.data, 1)
            
            for pred, actual in zip(predicted, labels):
                predicted_class = classes[int(pred)]
                actual_class = classes[int(actual)]
                total_samples[actual_class] += 1
                if predicted_class == actual_class:
                    correct_predictions[actual_class] += 1
            total += labels.size(0)
            correct += (predicted == labels).sum().item()
            #print('GroundTruth: ', ' '.join('%5s' % classes[predicted[j]] for j in range(4)))
    for class_name in classes:
        accuracy = 100 * correct_predictions[class_name] / total_samples[class_name]
        print(f'Accuracy for {class_name}: {accuracy:.2f}%')