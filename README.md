# psb6351_env

## Welcome to the PSB6351 class repository

We will use this repo to share code, submit homework assignments, and setup your environments

To begin you will need to setup git on your High Performance Computer (HPC) account

1. [Set up](https://help.github.com/articles/set-up-git/) git on HPC

    Perform steps 2-4 in Setting up git.

2. Set up your ssh [key](https://help.github.com/articles/connecting-to-github-with-ssh/)

    Make your passkey easy to remember.
    First Generate a new SSH key - Follow steps 1-4
    
    Next add your ssh key to your github account - Follow steps 1-8
    
    Next test your SSH connection - Follow steps 1-5

3. Modify your ~/.ssh/config file

    ```bash
    ssh -T -p 443 git@ssh.github.com
    ```
    
    You should see:
    
    > Hi username! You've successfully authenticated, but GitHub does not provide shell access.
    
    Add the following lines to your ~/.ssh/config file
    
    ```bash
    vi ~/.ssh/config
    ```

    Host github.com
    
    Hostname ssh.github.com
    
    Port 443
    
4. Fork the psb6351_env repository

    In a terminal type
    
    ```bash
    cd place/to/keep/repository
    git clone ssh://git@github.com/PSB6351/psb6351_env.git
    cd psb6351_env
    git remote add upstream ssh://git@github.com/PSB6351/psb6351_env.git
    ```
5. Chane repo configuration to ssh

    Open .git/config
    
    find url= entry under section [remote "origin"]
    
    Change it from 
    
    url=https://github.com/PSB6351/psb6351_env.git
    
    to
    
    ssh://git@github.com/PSB6351/psb6351_env.git
    
    
    
