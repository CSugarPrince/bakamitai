3/6/2021
Issue installing requirements.txt

- matplotlib 2.2.2 causing error. Incompatibility with curr version of Python3 (3.8.3)
  - Will try installing latest Python3 (3.9.2)
    1. C:\Users\guru\AppData\Local\Programs\Python\Python39
    1. virtualenv --python=C:\Users\guru\AppData\Local\Programs\Python\Python39\python.exe .
    1. Scripts\activate
    1. pip install -r requirements.txt
    1. No dice
  - Will tryinstalling older version of Python3 (3.4.4)
    1. virtualenv --python=C:\Python34\python.exe .
    1. same as above
    1. works... but now have a compatibility issue with pandas (0.23.4)
  - Will tryinstalling older version of Python3 (3.6.8)
    1. virtualenv --python=C:\Users\guru\AppData\Local\Programs\Python\Python36\python.exe .
    1. torch=1.0.0
  - Will tryinstalling older version of Python3 (3.5.4)
    1. virtualenv --python=C:\Users\guru\AppData\Local\Programs\Python\Python35\python.exe .
    1. torch==1.0.0
  - I give up. Trying Docker next. Will fiddle with Anaconda later.

Package Installation
conda 4.9.2
Anaconda Prompt
cd /d E:\Dev\first-order-model
conda create -p ./envs python=3.6.8
conda activate E:\Dev\first-order-model\envs

pip install -r requirements_2.txt
pip install torch==1.0.0 torchvision==0.2.1 -f https://download.pytorch.org/whl/torch_stable.html
conda list

Run Demo: (In Aconda Env:)
python demo.py --config config/vox-256.yaml --driving_video bakamitai_template.mp4 --source_image pic.jpg --checkpoint vox-cpk.pth.tar --relative --adapt_scale

conda install ffmpeg -c conda-forge

running again...

```
driving = torch.tensor(np.array(driving_video)[np.newaxis].astype(np.float32)).permute(0, 4, 1, 2, 3)
MemoryError
```

[open issue on original repo](https://github.com/AliaksandrSiarohin/first-order-model/issues/177)
[refactored code](https://gist.github.com/japanvik/71313bbcdb9eb099492bc6a8094abe8c)

python demo_refactored.py

```
site-packages\torch\nn\modules\conv.py", line 320, in forward
    self.padding, self.dilation, self.groups)
RuntimeError: cuDNN error: CUDNN_STATUS_EXECUTION_FAILED
```

[possible solution #1 to cuda issue](https://discuss.pytorch.org/t/cudnn-status-execution-failed-error/38575)

using cpu - took 42 minutes

[good article on resizing vs cropping](https://www.advisorwebsites.com/blog/blog/design/resizing-and-cropping-images-do-you-know-the-difference#:~:text=Resizing%20is%20used%20to%20bring,crop%20if%20it%20is%20necessary.)

Running on mac:
`/opt/anaconda3/envs/bakamitai/lib/python3.6/importlib/_bootstrap.py:219: RuntimeWarning: numpy.dtype size changed, may indicate binary incompatibility. Expected 96, got 88`
[resolved](https://github.com/numpy/numpy/issues/11788)

Test: Need to make sure output directory exists.
`FileNotFoundError: The directory '/Users/josh/Dev/dame-da-ne/output' does not exist`

python demo_refactored.py
Already taking less time (Est: 32 min)

3/15/2021
conda init changes the bashrc. Can be easily reversed by doing conda init --reverse

pip install moviepy error:
package incompatibility between moviepy and an older version of numpy:
`ERROR: pip's dependency resolver does not currently take into account all the packages that are installed. This behaviour is the source of the following dependency conflicts. moviepy 1.0.3 requires numpy>=1.17.3; python_version != "2.7", but you have numpy 1.15.0 which is incompatible.`

Also, am worried that package versions previously installed might have been overwritten by this pip install.

Will try conda install to fix compatibility issues:
[conda vs pip](https://www.anaconda.com/blog/understanding-conda-and-pip)

conda install -c conda-forge moviepy

hmm, will have to test recreating this environment.

3/16/2021
conda create -n test2 python=3.6.8

pip install -r requirements.txt
pip install torch==1.0.0 torchvision==0.2.1 -f https://download.pytorch.org/whl/torch_stable.html
conda install ffmpeg -c conda-forge

... wow, now no envs work... what was the point of making envs if packages managed to screw all of them up?

God, starting from scratch with packages
conda install --file requirements_test.txt
conda install -c pytorch torchvision
conda install -c conda-forge imageio-ffmpeg

python demo_refactored.py only took 20 min this time!
python add_music.py

Nice! Will freeze packages then commit. 
Will create another env and test again to confirm b4 committing.

conda list export > requirements_conda.txt
conda env export > environment.yml
pip freeze > requirements_shit.txt

3/18/2021
Will test:
get rid of `prefix: /opt/anaconda3/envs/bakamitai` for cross compatibility
conda env create -f environment.yml

environment created, will commit and test if it works on Windows

Issue on Windows. conda envs are not cross platform.
To get raw dependencies, had to do:
- go into 'shit' env
- conda env export --from-history > win_environment.yaml

every package I install from now on, I will have to add to

3/20/2021
Need to test making a docker container that runs code on GPU so that code runs in less than 5 seconds?
[ubunu image with cuda and conda](https://hub.docker.com/r/kundajelab/cuda-anaconda-base/)

replaced miniconda version to match version I am currently using.
docker build -t test .
docker run -i -t test /bin/bash

## 3/24/2021
Installed conda packages in docker conatainer.
Need to copy files over and test that it runs properly.

## 3/25/2021
docker ran the process extremely fast: 6 min... Why?

verifying:
docker cp silly_jang:/app/output/output.mp4 ./output/d_output.mp4

Everything is good. Nice.

Need to make environment.yml file for docker... when final version is done. until then, I will keep package intallation history in an install log.

## 3/26/2021
TODO
- Play with ECS. 
- Deploy container to ECS
- ssh an run app in cpu mode. log time.
- Update code to use GPU.
- Test rolling update
- Run app in GPU mode. log time.

docker context create ecs myecscontext
docker context ls
docker context use myecscontext

docker compose up

To look up:
- Docker compose
- Does my app need an EBS volume? Max IO option?
- Does it need Autoscaling?
- "overlays". Do I need to create a custom cft and specify it to get a GPU based EC2?
- Local simulation `docker context create ecs --local-simulation ecsLocal`. Facilitates dev and debug if code integrates with other AWS services.

## 3/27/2021
continued

docker compose up 
Error:
`NoCredentialProviders: no valid providers in chain. Deprecated.
For verbose messaging see aws.Config.CredentialsChainVerboseErrors`

probably because of how Docker integrates with AWS. it expects me to have Access and Secret key for this account on my machine...?

Try with context on root acc.

docker context rm myecscontext

same. 
Try creating using access key instead of profile.
works.

Try docker compose up
Error: 
`WARNING services.build: unsupported attribute        
service bakamitai doesn't define a Docker image to run: incompatible attribute`

Figure out how to tell compose to build image locally using Dockerfile.
Else, use Amazon ECR and store image there.

TODO
- use git-LFSs
- put image on ECR

## 3/29/2021
Forget git-LFS.
Using google drive folder with ADD command in Dockerfile to fetch the tar files.
Better. 
Also moving to new repository, so I don't have to undo git-LFS and stuff in this one.

## 3/30/2021
push to ECR from cli.
Authenticate docker to default registry:
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 073860560971.dkr.ecr.us-east-1.amazonaws.com

Login success

create a repository:
aws ecr create-repository \
    --repository-name bakamitai \
    --image-scanning-configuration scanOnPush=true \
    --region us-east-1

output:
{
    "repository": {
        "repositoryArn": "arn:aws:ecr:us-east-1:073860560971:repository/bakamitai",
        "registryId": "073860560971",
        "repositoryName": "bakamitai",
        "repositoryUri": "073860560971.dkr.ecr.us-east-1.amazonaws.com/bakamitai",
        "createdAt": "2021-03-30T20:13:58-04:00",
        "imageTagMutability": "MUTABLE",
        "imageScanningConfiguration": {
            "scanOnPush": true
        },
        "encryptionConfiguration": {
            "encryptionType": "AES256"
        }
    }
}

Tag and push
docker tag test2:latest 073860560971.dkr.ecr.us-east-1.amazonaws.com/bakamitai:latest
docker push 073860560971.dkr.ecr.us-east-1.amazonaws.com/bakamitai:latest

## 3/31/2021
TODO
- Deploy to ECS
- ssh and run code

TIL MiB means mebibyte or 1,048,576 bytes

ECS notes:
- Tasks are the unit of deployment. Contains one or more containers. 
- We don't run containers, we run tasks
- Fargate: 
  - charged whenever a task is run
  - each task run on its own stack of resources. Dopesn't share underlying kernel, cpu, mem (for ex) with other tasks
- EC2: 
  - we own and manage EC2s. charged for EC2 uptime and usage
  - each task can run on the same EC2. Doesn't can share underlying kernel, cpu, mem (for ex) with other tasks
- In both, containers share resources with other containers inside the same task... presumably


ECS
Container definition:
Container name: test
Image: 073860560971.dkr.ecr.us-east-1.amazonaws.com/bakamitai

Advanced container configuration/Environment
- GPUs: 1 
- Working directory: /app

Task definition:
Task definition name: test-task
Task memory: 16GB
Task CPU: 2 vCPU

Service definition:
default, no load balancer

... is there way to docker run -i -t into a task's container?
[running -it on ecs container](https://aws.amazon.com/blogs/containers/new-using-amazon-ecs-exec-access-your-containers-fargate-ec2/)

[using gpu ec2s on ecs](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ecs-gpu.html)

## 4/2/2021
I think right now... I will focus on getting a local cpu release out. Do GPU, web server stuff later.

TODO:
- refactor code
- create environment files for local cpu usage for windows, mac, docker
- write first blog about solving dependency hell with conda

Making the Win conda environment

cd /d E:\Dev\bakamitai
