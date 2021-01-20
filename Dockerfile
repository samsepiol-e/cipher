FROM python:3.7.6
WORKDIR /cipher
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY ./* ./
ENV HOME /home
RUN ["apt-get", "update"]
RUN ["apt-get", "install", "-y", "curl", "wget", "git"]
RUN sh -c "$(wget -O- https://raw.githubusercontent.com/samsepiol-e/configfiles/v3.0/zshinstall.sh)"
#RUN git clone https://github.com/VundleVim/Vundle.vim.git ~/.vim/bundle/Vundle.vim
#RUN curl https://raw.githubusercontent.com/samsepiol-e/configfiles/master/.vimrc >> $HOME/.vimrc
#RUN vim +PluginInstall +qall
