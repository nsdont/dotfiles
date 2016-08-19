#!/usr/bin/env bash

install_fzf () {
  if [ ! -d ~/.fzf ]
  then
    info 'installing fzf'
    git clone --depth 1 https://github.com/junegunn/fzf.git ~/.fzf
    ~/.fzf/install --no-update-rc --key-bindings --completion
  fi
}

install_fzf
