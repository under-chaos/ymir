## Introduction

English | [Simplified Chinese](README_zh-CN.md)

![YMIR](docs/images/YMIR.jpeg)

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**Catalog**

- [Citations](#citations)
- [1. Introduction to AI SUITE-YMIR](#1-introduction-to-ai-suite-ymir)
  - [1.1. Main functions](#11-main-functions)
  - [1.2. Apply for trial](#12-apply-for-trial)
- [2. Installation](#2-installation)
  - [2.1. Environment dependencies](#21-environment-dependencies)
  - [2.2. Installation of YMIR-GUI](#22-installation-of-ymir-gui)
  - [2.3. Installation of label studio (optional)](#23-installation-of-label-studio-optional)
- [3. Use YMIR-GUI: typical model production process](#3-use-ymir-gui-typical-model-production-process)
  - [3.1. Raw data preparation](#31-raw-data-preparation)
  - [3.2. Data labeling](#32-data-labeling)
  - [3.3. Model training](#33-model-training)
  - [3.4. Data mining](#34-data-mining)
  - [3.5. Model iteration](#35-model-iteration)
  - [3.6. Model validation](#36-model-validation)
  - [3.7. Model download](#37-model-download)
- [4. For advanced users: YMIR-CMD (command line) user's guide](#4-for-advanced-users-ymir-cmd-command-line-users-guide)
  - [4.1 Installation](#41-installation)
  - [4.2 Typical model production process](#42-typical-model-production-process)
    - [4.2.1 Preparation of external data](#421-preparation-of-external-data)
    - [4.2.2 Create local repo and import data](#422-create-local-repo-and-import-data)
    - [4.2.3 Merge and filter](#423-merge-and-filter)
    - [4.2.4 Train the initial model](#424-train-the-initial-model)
    - [4.2.5 Data mining](#425-data-mining)
    - [4.2.6 Data labeling](#426-data-labeling)
    - [4.2.7 Model iteration-data merging](#427-model-iteration-data-merging)
    - [4.2.8 Model iteration-model training](#428-model-iteration-model-training)
  - [4.3. YMIR-CMD manual](#43-ymir-cmd-manual)
- [5. Get the code](#5-get-the-code)
  - [5.1. YMIR repos](#51-ymir-repos)
  - [5.2. Code contribution](#52-code-contribution)
  - [5.3. About training, inference and mining docker images](#53-about-training-inference-and-mining-docker-images)
- [6. Design concept](#6-design-concept)
  - [6.1. Life of a dataset](#61-life-of-a-dataset)
    - [6.1.1. Introduction to a dataset](#611-introduction-to-a-dataset)
    - [6.1.2. Branch and dataset management](#612-branch-and-dataset-management)
- [7. MISC](#7-misc)
  - [7.1. FAQ](#71-faq)
  - [7.2. License](#72-license)
  - [7.3. Contact us](#73-contact-us)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

# Citations

If you wish to refer to YMIR in your work, please use the following BibTeX entry.
```bibtex
@inproceedings{huang2021ymir,
      title={YMIR: A Rapid Data-centric Development Platform for Vision Applications}, 
      author={Phoenix X. Huang and Wenze Hu and William Brendel and Manmohan Chandraker and Li-Jia Li and Xiaoyu Wang},
      booktitle={Proceedings of the Data-Centric AI Workshop at NeurIPS},
      year={2021},
}
```

# 1. Introduction to AI SUITE-YMIR

As a streamlined model development product, YMIR(You Mine In Recursion) focuses on the dataset versioning and model iteration in the AI SUITE open-source series.

AI commercialization is currently reaching a stage of maturity in terms of computing hardwares,  algorithms, etc. The adoption of AI often encounter challenges such as a lack of skilled developers, high development costs, and long iteration cycles.

As a platform, YMIR provides an end-to-end AI development system. This platform reduces costs for companies using artificial intelligence and accelerates the adoption of artificial intelligence. YMIR provides ML developers with one-stop services for data processing, model training, and other steps required in the AI development cycle.

The YMIR platform provides effective model development capabilities with a data-centric approach. The platform integrates concepts such as active learning methods, data and model version control, and workspace. Parallel rapid iteration of data sets and projects for multiple specific tasks are realized by YMIR. The platform uses an open API design, so third-party tools can also be integrated into the system.

## 1.1. Main functions

A typical model development process can usually be summarized in a few steps: defining the task, preparing the data, training the model, evaluating the model, and deploying the model.

*  Define the task: Before starting an AI development project, it is important to be clear about what is to be analyzed. This will help developers correctly convert the problem into several typical ML modeling tasks, such as image classification, object detection, etc. Different tasks have different data requirements.

*  Prepare data: Data preparation is the foundation of a successful AI project. The most important task in this step is to ensure the quality of data and its annotations. Collect all the required data at the beginning is the optimal situation for many projects. Therefore, the project developer may find that some data is missing in subsequent stages. Additional data could be necessary upon the project  needs.

*  Train model: This operation is commonly referred to "modeling". This step refers to the exploration and analysis of prepared data to discover the internal patterns and any links between the input and the expected prediction target.  The result of this step is usually one or more machine learning models. These models can be applied to new data to obtain predictions. Developers train their own models using mainstream model training frameworks, such as pytorch, tensorflow, darknet, etc.

*  Evaluate model: The entire development process has not yet been completed after training the model. Models need to be evaluated and checked before being put into production. Normally, get a production-quality model all at once is not so easy. You need to adjust parameters, and iterate the model continuously. Some common metrics can help you evaluate models quantitatively and pick a satisfactory model. Some common metrics can help you to evaluate models quantitatively.

*  Deploy model: Models are developed and trained based on previously available data (possibly test data). After a satisfactory model is obtained, it will be applied to real data to make predictions at scale.

The YMIR platform mainly meets the needs of users for developing models at scale. The platform provides users an easy-to-use user interface, it is consists of four parts: home page, task management, dataset management, and model management, which have the following main functions:

| Function Module    | Primary Function  | Function Description                                         |
| ------------------ | ----------------- | ------------------------------------------------------------ |
| Dataset management | Dataset importing | Copy public datasets, URL addresses, path imports, and local imports to assist users in importing prepared datasets |
| Dataset management | Dataset viewing   | Visualization of image data and annotations, and check history information |
| Dataset management | Dataset editing   | Operations like dataset edit, delete, etc.                   |
| Task management    | Filter task       | Filtering the data by tags                                   |
| Task management    | Training task     | Support self-selected datasets, labels, adjust training parameters for model training, check corresponding results after task completion |
| Task management    | Mining task       | Find the most beneficial data for model optimization         |
| Task management    | Labeling task     | Add annotations to image data                                |
| Model management   | Model validation  | Upload an image to check the performance of a model          |



## 1.2. Apply for trial

We provide an online trial version for your convenience. If you need, please fill out the [Apply for YMIR Trial](https://alfrat.wufoo.com/forms/mkxsic906al0pf/) , and we will send the trial information to your email address.

# 2. Installation

![process](docs/images/process.jpeg)

How do users choose to install GUI or CMD?

1. The GUI verision with the supports of model training and model iteration is more suitable for ordinary users.

2. If you need to modify the default configuration of the system, such as customizing labels and replacing training algorithms, it is recommended to install CMD;

This chapter contains the installation instructions for YMIR-GUI. If you need to use CMD, please refer to the [Ymir-CMD user guide] (#4-for-advanced-users-ymir-cmd-command-line-users-guide).

## 2.1. Environment dependencies

1.NVIDIA drivers shall be properly installed before installing YMIR. For detailed instructions, see https://www.nvidia.cn/geforce/drivers/.

2. Docker installation:

* Installation of Docker and Docker Compose https://docs.docker.com/get-docker/

* Installation of NVIDIA Docker https://github.com/NVIDIA/nvidia-docker

3. Hardware Suggestions

* NVIDIA GeForce RTX 2080 Ti or higher is recommended.

## 2.2. Installation of YMIR-GUI

The user must ensure that all the conditions in [Cuda environment dependencies] (#21-cuda-environment-dependencies) have been met, otherwise the installation may fail.

The YMIR-GUI project package is on DockerHub and the steps to install and deploy YMIR are as follows:

1.  Clone the deployment project YMIR to the local server:

  ```sh
git clone git@github.com:IndustryEssentials/ymir.git
  ```

2. In the cloned YMIR folder, install and start the service by typing:

  ```sh
sh ymir.sh start
  ```

After the service is started successfully, YMIR will be available at [http://localhost:12001/](http://localhost:12001/). If you need to **stop the service**, run the command: `sh ymir.sh stop`

## 2.3. Installation of label studio (optional)

Label Studio is an external labeling system that works with YMIR. Install it if you plan to label data in the development process.

1. In the YMIR directory, start the installation command:

  ```sh
docker-compose -f docker-compose-component.yml up -d
  ```

2. Check the status of label studio:

  ```sh
docker-compose -f docker-compose-component.yml ps
  ```

The user can access label studio through the default URL [http://localhost:12007/] (http://localhost:12007/). The installation is successful if the login page shows up.

3. Configure the label studio authorization token

  After the user registers and log in to Label Studio, select "Account & Settings" in the upper right corner of the page. Then, copy the token value and paste it into the corresponding location (LABEL_STUDIO_TOKEN) in the .env configuration file of the YMIR project. An example is as follows:

  ```sh
  label studio env

  LABEL_STUDIO_OPEN_HOST=http://xxx.xxx.xx.xxx

  LABEL_STUDIO_OPEN_PORT=12007

  LABEL_STUDIO_TOKEN="Token token_value"

  LABEL_TASK_LOOP_SECONDS=60
  ```

  Restart ymir after configuring the host address (LABEL_STUDIO_OPEN_HOST) and the token (LABEL_STUDIO_TOKEN).

4. The command to stop the label studio service is:

  ```sh
docker-compose -f docker-compose-component.yml down
  ```

# 3. Use YMIR-GUI: typical model production process

This section uses a complete model iteration process as an example to illustrate how to use the YMIR platform.

![YMIR-GUI process](docs/images/YMIR-GUI-process.jpeg)

As shown in the figure above, YMIR divides the model development process into multiple steps. Details about how to run each step are listed in the subsequent sections.

## 3.1. Raw data preparation

The user prepares a dataset with training targets (training set and test set) for training an initial model. Before importing, please ensure that the format of the dataset meets the following requirements:

*  The dataset is in.zip format, it should contain two folders named as "images" and "annotations" respectively;
*  Images: create an ''images'' folder and place images in it. The formats currently supported by this platform are limited to jpg, jpeg, and png;
*  Annotations: create an "annotations" folder and place annotation files formatted as [Pascal VOC](http://host.robots.ox.ac.uk/pascal/VOC/voc2012/htmldoc/devkit_doc.html#SECTION00093000000000000000) (if there are no annotation files, leave the folder empty);
*  For a labeled dataset, the labeled object type must belong to the built-in label list of the platform. Please click the link to view the detailed tag list, [Tag List] (https://github.com/IndustryEssentials/ymir-proto/blob/master/ymir/ids/type_id_names.csv) for details;
*  If users need custom tags, please see [How to Modify the Category Name Tag File] (#71-faq).

The platform supports four kinds of dataset importing: public dataset replication, network importing, local importing, and path importing.

![import guide](docs/images/import-guide.jpeg)

(1) public dataset replication: the user can copy the built-in dataset of the super administrator to the current operating user. The user can filter and import the label categories they need, as shown in the figure below:
![public dataset](docs/images/public-dataset.jpeg)

![public dataset2](docs/images/public-dataset2.jpeg)

Select the eligible dataset and click [OK] to start copying.

(2) Network import: users need to enter the URL path corresponding to the dataset as shown in the following:

![inter import](docs/images/inter-import.jpeg)

(3) Local import: users needs to upload a zip file of the local dataset in the following format. The zip size is recommended to be no more than 200MB.

Users can download the example **Sample.zip** for reference as follows:

![local import](docs/images/local-import.jpeg)

(4) Path Import: The user must enter the dataset's absolute path in the server, as shown in the figure below:

![path import](docs/images/path-import.jpeg)

Users can unpack and separate the training set (VOC2012_train), the test set (VOC2012_val), and the dataset to be mined (VOC2012_mining) from the open-source dataset VOC2012 ([click to download VOC2012](http://host.robots.ox.ac.uk/pascal/VOC/voc2012/VOCtrainval_11-May-2012.tar)) . The user needs to modify the folder names, then compress them into separate zip packages that meet the import requirements and import them by local import. As the following figures show:

![import success](docs/images/import-success.jpeg)

## 3.2. Data labeling

If the imported training set or test set does not have labels, users need to label them. Users can click the [Label] button on the task management page to jump to the Create Data Annotation Task interface as shown in the following figure.

![label1](docs/images/label1.jpeg)

The user must enter the task name, the dataset, the email address of the annotator, and the labeling target (person, car). If you want to check the labeling platform by yourself, please click "View on labeling platform" and fill in your labeling platform account. If you have more detailed requirements for the annotation, you can upload the annotation description document for the annotator's reference. You must register with the labeling system in advance. You can click "Register Labeling Platform Account" at the bottom to jump to the Label Studio labeling platform to register their labeling account. Click on Create Task, as shown in the figure below:

![label2](docs/images/label2.jpeg)

After successful creation, users can view the corresponding task progress and other information on the task management interface. After the task is completed, the YMIR will automatically retrieve the annotation results and generate a new dataset with the new annotation.

## 3.3. Model training

Click the [Train] button in the task management interface to jump to the Create Model Training Task interface, as shown in the following figure:

![train1](docs/images/train1.jpeg)

The user needs to enter the needed information in the form above to configure a training task. The training parameters (a.k.a. hyper-parameters) are populated with default values and can be changed if necessary. Users can also add parameters by themselves. Then, click the [Create Task]. As shown in the figure below, the initial model is trained.

![train2](docs/images/train2.jpeg)

After successful creation, users can view the corresponding task progress and information on the task management page. Users can view the accuracy of the trained model (mAP value) after the task is completed.



- **Model iterations (Improve accuracy through iteration)**

## 3.4. Data mining

YMIR provides data mining algorithms that support million-level data mining to quickly find the most favorite data for model optimization.

The user can use the model obtained from the initial training to perform data mining on the dataset to be mined. Click the [Mining] button on the task management interface to jump to the Create Data Mining Task interface, as shown in the following figure:

![mine1](docs/images/mine1.jpeg)

The user needs to enter the task name, select the data set (VOC2012_mining), and select the model (the initial model trained as illustrated in previous section). The user must also enter the filter TOPK as 500 (the first 500 successfully mined images), and set custom parameters if necessary.

![mine2](docs/images/mine2.jpeg)

After a task is created, users can view the task progress and the result of the mining task on the task management page.

## 3.5. Model iteration

![process-en](docs/images/process-en.jpeg)

After the mining task is completed, the mined dataset (mine-voc, 500 images) is obtained from the dataset to be mined (VOC2012_mining). The mined dataset (mine-voc, 500 sheets) is labeled by repeating step [3.2 Data labeling] (#32-data-labeling)to obtain the labeled dataset (mine-voc-label, 500 sheets). The following figure shows:

![mine success](docs/images/merge-train2.jpeg)

After the labeling task is completed, the training task should be created again. The labeled dataset (mine-voc-label, 500 sheets) is merged with the original dataset (VOC2012_train, 8815 sheets). The process of creating training is shown in the figure below:

![merge train](docs/images/merge-train3.jpeg)

## 3.6. Model validation

After training the model, users can validate the model. On the [Model Management] page, you can click the [Verify] button of the corresponding model to jump to the [Model Validation] page. As shown in the following figure:

![model val1](docs/images/model-val1.jpeg)

![model val2](docs/images/model-val2.jpeg)

The user can click the [Upload Image] button and select a local image to upload. The result will be displayed as follows:

![model val3](docs/images/model-val3.jpeg)

Users can choose to download the trained model. Users can also choose to continue to use the model for mining. So as to enter the next round of data mining, data labeling, model training cycle, and further optimize the model.

## 3.7. Model download

Users can click the [Download] button on the [Model List] page. The downloaded file is a tar package, which contains the network structure of the model, network weights, hyper-parameter configuration files, training environment parameters, and results. As shown below:

![model download](docs/images/model-download.jpeg)

# 4. For advanced users: YMIR-CMD (command line) user's guide

This chapter contains the instructions for the YMIR-CMD. If you need to use the GUI, please refer to [Ymir-GUI Installation] (#2-installation).

## 4.1 Installation

**Mode I. Pip Installation**

```
# Requires >= Python3.7
$ pip install ymir-cmd
$ mir --vesion
```

**Mode II. Installation from the source**

```
$ git clone --recursive git@github.com:IndustryEssentials/ymir-cmd.git
$ cd ymir-cmd
$ python setup.py clean --all install
$ mir --version
```

## 4.2 Typical model production process

![process-en](docs/images/process-en.jpeg)

The above figure shows a typical process of model training: 1) the user prepares external data, 2) imports it into the system, 3) appropriately filters the data, and 4) begins training to obtain a model (possibly with low accuracy). 5) selects images in a dataset to be mined that are suitable for further training based on this model, 6) annotates these images, 7) merges the annotated results with the original training set, and 8) uses the merged results to run the training process again to obtain a better model.
This section implement the process shown above using the command line.
All the following commands are prefixed with $ (which is also the Linux prompt under the normal user). When entering a command in the console, the user does not need to enter $ at the same time.

### 4.2.1 Preparation of external data

The system has the following requirements for external data.

1. With [VOC annotations] (https://towardsdatascience.com/coco-data-format-for-object-detection-a4c5eaf518c5)

2. The paths to all images (collectively referred to as assets or media in this system) need to be written uniformly in the "index.tsv" file. All annotation files need to be in the same directory.

3. The user must have read access to "index.tsv," all images, and all annotation files.

We take the pascal 2017 test dataset as an example. Download the dataset "VOC2012test.tar" from the official website and unpack.

```
$ tar -xvf VOC2012test.tar
```

After unpacking, the following directory structure is available (assuming VOCdevkit is in the /data directory).

```
/data/VOCdevkit
` - VOC2012
    |-- Annotations
    |-- ImageSets
    |-- Action
    |-- Layout
    |-- Main
    | `-- Segmentation
    ` -- JPEGImages
```

Note that all annotations are in the annotations directory and all images are located in the JPEGImages directory.

Users can use the following command to generate the "index.tsv" file.

```
$ find /data/VOCdevkit/VOC2012/JPEGImages -type f > index.tsv
```

The generated "index.tsv" is as follows:

```
/data/VOCdevkit/VOC2012/JPEGImages/2009_001200.jpg
/data/VOCdevkit/VOC2012/JPEGImages/2009_004006.jpg
/data/VOCdevkit/VOC2012/JPEGImages/2008_006022.jpg
/data/VOCdevkit/VOC2012/JPEGImages/2008_006931.jpg
/data/VOCdevkit/VOC2012/JPEGImages/2009_003016.jpg
...
```

And this "index.tsv" can be used for the next step of data import.

In addition, each annotation in the Annotations folder has the same main file name as the image. One of the <name>xxx</name> attributes will be extracted as a predefined keyword to be used in a later step of data filtering.

### 4.2.2 Create local repo and import data

The command line on this system uses a method similar to Git to manage user resources. Users create their own mir repository and perform all the following tasks in this mir repo.

Use the following command to create a mir repo:

```
$ mkdir ~/mir-demo-repo && cd ~/mir-demo-repo # Create the directory and enter
$ mir init # init this directory to a mir repo
$ mkdir ~/ymir-assets ~/ymir-models # Creates assets and models storage directory, mir repo only keeps reference to assets and models
```

Users are required to prepare three data sets in advance.

1. A training set (for example, named "dataset-training"), with annotations, for initial model training.

2. A validation set (named "dataset-val") that includes annotations.

3. Mining set (named "dataset-mining"): a large dataset to be mined from.

The user imports the three data sets with the following command:

```
$ cd ~/mir-demo-repo
$ mir import --index-file /path/to/training-dataset-index.tsv \ # index.tsv path
             --annotation-dir /path/to/training-dataset-annotation-dir \ # annotations dir
             --gen-dir ~/ymir-assets \ # assets storage dir
             --dataset-name 'dataset-training' \ # dataset name
             --dst-rev 'dataset-training@import' # destination branch and task name
$ mir checkout master
$ mir import --index-file /path/to/val-dataset-index.tsv \
             --annotation-dir /path/to/val-dataset-annotation-dir \
             --gen-dir ~/ymir-assets \
             --dataset-name 'dataset-val' \
             --dst-rev 'dataset-val@import'
$ mir checkout master
$ mir import --index-file /path/to/mining-dataset-index.tsv \
             --annotation-dir /path/to/mining-dataset-annotation-dir \
             --gen-dir ~/ymir-assets \
             --dataset-name 'dataset-mining' \
             --dst-rev 'dataset-mining@import'
```

Users can use this command to see the branches of the current mir repo:

```
$ mir branch
```

This repo has four branches: master, dataset-training, dataset-val, and dataset-mining. The current repo is on the branch dataset-mining.

Users can also view the status of branch with:

```
$ mir show --src-rev dataset-mining
```

And output as follow:

```
person;cat;car;airplane

metadatas.mir: 200 assets, tr: 0, va: 0, te: 0, unknown: 200
annotations.mir: hid: import, 113 assets
tasks.mir: hid: import
```

The first and second rows are predefined keywords and custom keywords (in this output, there are no custom keywords). The next lines are the number of resources, the number of comments, and the status of tasks under the current branch.

### 4.2.3 Merge and filter

Users can merge dataset-training and dataset-val with:

```
$ mir merge --src-revs tr:dataset-training@import;va:dataset-val@import \ # source branches to be merged
            --dst-rev tr-va@merged \ # destination branch and task name
            -s host # conflicts resolve strategy: use infos on host branch (the first branch in --src-revs)
```

After the merge is complete, you can see that the current repo is under the tr-va branch and you can check the status with mir show:

```
$ mir show --src-revs HEAD # HEAD refers to the current head branch, and can be replaced by the specific branch name tr-va
```

The output is as follows:

```
person;cat;car;airplane

metadatas.mir: 3510 assets, tr: 2000, va: 1510, te: 0, unknown: 0
annotations.mir: hid: merged, 1515 assets
tasks.mir: hid: merged
```

If the dataset-training and dataset-val before merging have 2000 and 1510 images, you can see that the merge branch has 2000 images as the training set and 1510 images as the validation set.
If the user only wants to train the model to detect humans and cats, we first filter out the resources of humans and cats from the tr-va branch:

```
mir filter --src-revs tr-va@merged \
           --dst-rev tr-va@filtered \
           -p 'person;cat'
```

### 4.2.4 Train the initial model

First, users need to pull the training and mining docker images from the docker hub as follows:

```
docker pull industryessentials/executor-det-yolov4-training:release-0.1.2
docker pull industryessentials/executor-det-yolov4-mining:release-0.1.2
```

and start the training process with the following command:

```
mir train -w /tmp/ymir/training/train-0 \
          --media-location ~/ymir-assets \ # assets storage dir
          --model-location ~/ymir-models \ # model storage dir
          --config-file ~/training-config.yaml \ # training config file, get it from training docker image
          --src-revs tr-va@filtered \
          --dst-rev training-0@trained \
          --executor industryessentials/executor-det-yolov4-training:release-0.1.2 # docker image name
```

After the model training is completed, the system will output the model ID. The user can view the package file of the model in "/ymir-models".

### 4.2.5 Data mining

This model is trained on a small dataset, and users can get the best images for the next training step in this mining process with the following command:

```
mir mining --src-revs dataset-mining@import \ # mining dataset branch
           --dst-rev mining-0@mining \ # destination branch
           -w /tmp/ymir/mining/mining-0 \ # tmp working dir for this task
           --topk 200 \ # topk
           --model-location ~/ymir-models \
           --media-location ~/ymir-assets \
           --model-hash <hash> \ # model id
           --cache /tmp/ymir/cache \ # asset cache
           --config-file ~/mining-config.yaml \ # mining config file, get it from mining docker image
           --executor industryessentials/executor-det-yolov4-mining:release-0.1.2 # mining docker image name
```

### 4.2.6 Data labeling

Now the user has 200 images on the branch "mining-0". These images will be most useful in the next training step. The next task is to export these resources and send them to the annotators for labeling.

Users can export assets with the following command:

```
mir export --asset-dir /tmp/ymir/export/export-0/assets \ # export directory for assets
           --annotation-dir /tmp/ymir/export/export-0/annotations \ # export directory for annotations
           --media-location ~/ymir-assets \ # assets storage directory
           --src-revs mining-0@mining \
           --format none # no annotations needed
find /tmp/ymir/export/export-0/assets > /tmp/ymir/export/export-0/index.tsv
```

After the export is done, users can see images at /tmp/ymir/export/export-0/assets. Users can send these pictures for annotation, and the annotations need to be saved in VOC format (assuming the save path is still /tmp/ymir/export/export-0/annotations).
Once the annotation is finished, the user can import the data using a similar approach to the import command in [4.2.2](#422-create-local-repo-and-import-data).

```
$ mir import --index-file /tmp/ymir/export/export-0/index.tsv
             --annotation-dir /tmp/ymir/export/export-0/annotations \ # annotation directory
             --gen-dir ~/ymir-assets \ # asset storage directory
             --dataset-name 'dataset-mining' \ # dataset name
             --dst-rev 'labeled-0@import' # destination branch and task name
```

### 4.2.7 Model iteration-data merging

The branch "labeled-0" now contains the 200 new training images. Users can be merged together with the original training set by the merge command.

```
$ mir merge --src-revs tr-va@filtered;tr:labeled-0@import \ # source branch
            --dst-rev tr-va-1@merged \ # destination branch and task name
            -s host
```

### 4.2.8 Model iteration-model training

Now branch tr-va-1 contains the previous training and validation set and 200 new images we have just mined and labeled. A new model can be trained on this set with the following command:

```
mir train -w /tmp/ymir/training/train-1 \ # different working directory for each different training and mining task
          --media-location ~/ymir-assets \
          --model-location ~/ymir-models \
          --config-file ~/training-config.yaml \
          --src-revs tr-va-1@merged \ # use new-merged branch
          --dst-rev training-1@trained \
          --executor industryessentials/executor-det-yolov4-training:release-0.1.2
```

## 4.3. YMIR-CMD manual

YMIR-command-api.211028

**Common parameter format and definitions**

| Parameter Name | Variable Name | Type and Format | Definition                                                   |
| -------------- | ------------- | --------------- | ------------------------------------------------------------ |
| --root / -r    | mir_root      | str             | The path the user needs to initialize. If not specified, it is the current path. |
| --dst-rev      | dst_rev       | str             | 1. target-rev, single only                                   |
|                |               | rev@tid         | 2. All changes will be saved to this rev's tid               |
|                |               |                 | 3. If it is a new rev, checkout the first src-revs before creating |
|                |               |                 | 4. tid is required. rev is required.                         |
| --src-revs     | src_revs      | str             | 1. Multiple data source revisions separated by semicolons (only supported by merge, other cmd only support single) |
|                |               | typ:rev@bid     | 2. typ is optional. Only effective in merge and supports pre-use identifiers (tr/va/te). If typ is empty, it means that the settings in the original rev are used |
|                |               |                 | 3. bid is optional. If it is empty, read the head task id    |
|                |               |                 | 4. rev cannot be empty                                       |
|                |               |                 | Note: When there are multiple revs, e.g. a1@b1; a2@b2, you need to enclose them in quotes because the semicolon is a Linux command separator |

**mir init**

| DESCRIPTION                                                  |          |               |
| ------------------------------------------------------------ | -------- | ------------- |
| mir init [--root <mir_root>]                                 |          |               |
| Initialize the current path, or the path specified by -root as a mir root |          |               |
| ARGS (name of ARGS, name, type, description of arguments in run_with_args) |          |               |
| --root / -r                                                  | mir_root | str, optional |
| RETURNS                                                      |          |               |
| Normal initialization: returns 0                             |          |               |
| Exception: other error code                                  |          |               |

**mir branch**

| DESCRIPTION                    |          |               |
| ------------------------------ | -------- | ------------- |
| mir branch [--root <mir_root>] |          |               |
| List all local branches        |          |               |
| ARGS                           |          |               |
| --root / -r                    | mir_root | str, optional |
| RETURNS                        |          |               |

# 5. Get the code

## 5.1. YMIR repos

The YMIR project consists of three components:

1. [Back-end](https://github.com/IndustryEssentials/ymir/tree/master/ymir/backend), task distribution and management.

2. [Front-end](https://github.com/IndustryEssentials/ymir/tree/master/ymir/web), interactive interface.

3. [Command line](https://github.com/IndustryEssentials/ymir/tree/master/ymir/command), a command-line interface (CLI) for managing the underlying annotation and image data.

## 5.2. Code contribution

Any code in the YMIR repo should follow the coding standards and will be checked in the CI tests.

- Functional code needs to be unit tested.

- Use [flake8](https://flake8.pycqa.org/en/latest/) or [black](https://github.com/ambv/black) to format the code before committing. Both of these follow the [PEP8](https://www.python.org/dev/peps/pep-0008) and [Google Python Style](https://google.github.io/styleguide/pyguide.html) style guides.

- [mypy](http://mypy-lang.org/) - Python must go through static type checking.

Also check out [MSFT Encoding Style](https://github.com/Microsoft/Recommenders/wiki/Coding-Guidelines) for more advice.

## 5.3 About training, inference and mining docker images

[Check this document](docs/ymir-cmd-container.md) for details

# 6. Design concept

## 6.1. Life of a dataset

### 6.1.1. Introduction to a dataset

The dataset consists of metadata and media files, and the metadata has the following characteristics:

* A unique ID and the system has an initial default metadata status of null.

* A list of resources, where each element points to an actual resource; Metadata doesn't actually hold resources, but only maintains this list of resources.

* A number of keywords by which a user can search for a particular metadata status.

* Support users to create a new metadata branch and perform operations on the newly created branch. The operations on the new branch do not affect the status of the original metadata, and the original metadata is still traceable by the user. These operations include but are not limited to the following:

  (1) Adding resources
  (2) Adding or modifying annotations
  (3) Add or modify keywords
  (4) Filtering resources
  (5) Merging two different metadatas

* You can switch freely between different metadata.

* You can query the history of the metadata.

* You can tag the metadata to facilitate precise search by tag.

* You can also add keywords to metadata to facilitate fuzzy search through keywords.

* You can read the resources contained in a metadata and use those resources for browsing, training and so on.

From the above description, it can be seen that the management of metadata is similar to that of VCS (Version Control System), and users can have the following completely different usage methods and scenarios:

**The first scene**: Directly from the very first metadata, a filtering process is carried out to select and use the data that meets the requirements, as shown in the following figure:

![Scenario1](docs/images/Scenario1.jpeg)

Whenever the user needs to start a new task,
:: The user checks out a new feature branch from within the current master branch, getting the metadata in feature#1 state.
:: The user performs data filtering and other tasks on the metadata of this new branch. The user can obtain the metadata in the feature #2 state.
:: When it is confirmed that this metadata is suitable for the user's training task, then the user can start training using this data.

* At this point, changes made by other users to the master branch's metadata will not affect the training data the user is using either.

**The second scene**: Search for certain metadata by tag or keyword. The user starts the screening process until the data meets the requirements, and then the data is used. As shown below:

![Scenario2](docs/images/Scenario2.jpeg)

At this point, whenever a user needs to carry out a new task,
:: Users can search for metadata that basically matches the user's requirements by means of keywords, tags, and so on.
:: On this basis, users need sign out a new branch.
:: Users can continue data filtering or cleansing on the new branch to obtain data that actually meets the requirements.
:: Users can use this data for training.

**The third scene**: incremental merging. Suppose the user has completed the training task of the model using certain metadata. At this point, there is an update to the metadata of the repository and the master branch. The user wishes to merge this part of the update into the currently used metadata.

![Scenario3](docs/images/Scenario3.jpeg)

Suppose the user is now in FEATURE#2 and needs to do the following:
:: You need switch back to master branch master.
:: You need repeat the task previously done for the incremental part master#2 - master#1 to obtain feature#2+.
:: You need cut back to feature#2 and merge feature#2+ to get feature#3.

### 6.1.2. Branch and dataset management

The discussion in this section is based on the following assumptions:
:: The user's data is imported in batches in units of datasets.
:: Each dataset is a separate branch.
:: Changes to and maintenance of each dataset are carried out on this branch.
:: Master branch is always empty.
This management approach is shown in the following figure:

![branch and dataset](docs/images/branch-and-dataset.jpeg)

We use the concept of code version control in Git to manage our data and models, use the concept of branches to create new projects so that different tasks on the same set of images can run in parallel. The additions, retrievals, updates, and deletions of datasets and basic operations are created by commits to branches. Logically, each commit stores an updated version of the dataset or new model, as well as the metadata of the operation that led to this change. Finally, only the data changes are merged into the main branch. This branch conceptually aggregates all the data annotated by many projects on the platform.

# 7. MISC

## 7.1. FAQ

**Why did the upload of the local dataset fail?**

Regardless of whether the dataset has a label file, the images folder and annotations folder must be created. The images are placed in the images folder and the format is limited to jpg, jpeg, and png. The annotation files are placed in the annotations folder and the format is the pascal (when there is no annotation file, the folder is empty). Please put the images and annotations in the same folder and compress them into a ".zip" compressed package (not a .rar compressed format).

**How should I obtain training and mining configuration files?**

The default profile template needs to be extracted in the mirror.

The training image `industryessentials/executor-det-yolov4-training:release-0.1.2` has a configuration file template located at: `/img-man/training-template.yaml`

Mining and inference mirrors The configuration file templates for `industryessentials/executor-det-yolov4-mining:release-0.1.2` are located at: `/img-man/mining-template.yaml` (mining) and `/img-man/infer-template. yaml` (infer)

**How can the trained model be used outside the system?**

After successful training, the system will output the ID of the model. The user can find the corresponding file according to this id at `--model-location`. In fact, it is a tar file that can be extracted directly using the tar command to get the "mxnet" model file in parameters and JSON format.

**How to view and modify the label file of the category name?**

This file is in the package installation directory. Use this command to view the content of this file:

```
cat `pip show ymir-proto | grep 'Location: ' | cut -d ' ' -f2`/ymir/ids/type_id_names.csv
```

And you may get output like this:

```
0,frisbee
1,car
2,person
3,surfboard
4,cat
5,bed
6,clock
7,pizza,pizza pie
8,skateboard
9,dining table,diningtable,board
```

Each line of this configuration file is separated by commas. The first item is the category id, followed by the category name.

Pay attention to this line with id 7. It has 3 items: "7, pizza, and pizza pie". The first one is category id, the second one is a category name, and the third one is category alias.

In the filter command, the -c and -C arguments are mapped to category ids with this file. All category aliases have the same meaning as category names.

You can edit this file by vi and other text editing tools. You can add alias to category or add new category, but it is not recommended to change the primary id and name of category that already existed.

## 7.2. License

YMIR is licensed under version 2.0 of the Apache License. See the [LICENSE](https://github.com/IndustryEssentials/ymir/blob/master/LICENSE) file for details.

## 7.3. Contact us

Contact us with further questions：contact.viesc@gmail.com

<!-- ALL-CONTRIBUTORS-BADGE:START - Do not remove or modify this section -->
[![All Contributors](https://img.shields.io/badge/All%20Contributors-8-brightgreen)](#contributors-)
<!-- ALL-CONTRIBUTORS-BADGE:END -->

<a href="https://github.com/phoenix-xhuang"><img src="https://avatars.githubusercontent.com/u/89957974?v=4" class="avatar-user" width="18px;"/></a> 
<a href="https://github.com/IJtLJZ8Rm4Yr"><img src="https://avatars.githubusercontent.com/u/90443055?v=4" class="avatar-user" width="18px;"/></a> 
<a href="https://github.com/elliotmessi"><img src="https://avatars.githubusercontent.com/u/90443217?v=4" class="avatar-user" width="18px;"/></a> 
<a href="https://github.com/Aryalfrat"><img src="https://avatars.githubusercontent.com/u/90443348?v=4" class="avatar-user" width="18px;"/></a> 
<a href="https://github.com/fenrir-z"><img src="https://avatars.githubusercontent.com/u/90444968?v=4" class="avatar-user" width="18px;"/></a> 
<a href="https://github.com/under-chaos"><img src="https://avatars.githubusercontent.com/u/90446262?v=4" class="avatar-user" width="18px;"/></a> 
<a href="https://github.com/Zhang-SJ930104"><img src="https://avatars.githubusercontent.com/u/91466580?v=4" class="avatar-user" width="18px;"/></a> 
<a href="https://github.com/LuciferZap"><img src="https://avatars.githubusercontent.com/u/92283801?v=4" class="avatar-user" width="18px;"/></a> 
