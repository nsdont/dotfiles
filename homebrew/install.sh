# !/bin/sh
#
# Homebrew
#
# This installs some of the common dependencies needed (or at least desired)
# using Homebrew.

# Binaries
binaries=(
  ack
  aircrack-ng
  aria2
  asciinema
  autoconf
  autoenv
  autojump
  chromedriver
  cmake
  coreutils
  curl
  ctags
  erlang
  freetype
  highlight
  htop-osx
  go
  git
  git-flow
  gettext
  goaccess
  graphviz
  htop-osx
  imgcat
  redis
  jpeg
  libevent
  libffi
  libxml++
  libmagic
  libpng
  libtiff
  libyaml
  ruby
  openjpeg
  macvim
  mackup
  mysql
  mosh
  m-cli
  nginx
  nmap
  node
  openjpeg
  openssl
  postgresql
  pyenv
  python
  python3
  rabbitmq
  redis
  ssh-copy-id
  sqlite
  the_silver_searcher
  thefuck
  trash
  tree
  vim
  wget
  zsh
  zsh-completions
)

# Apps
apps=(
  1password
  alfred
  anki
  bartender
  bilibili
  calibre
  charles
  daisydisk
  dash
  dropbox
  docker
  evernote
  flux
  fantastical
  gas-mask
  google-chrome
  iina
  istat-menus
  iterm2
  keka
  kindle
  licecap
  manico
  moom
  omnifocus
  omnigraffle
  omnioutliner
  omniplan
  openemu
  paw
  qlcolorcode
  qlimagesize
  qlprettypatch
  qlmarkdown
  qlstephen
  qlvideo
  quicklook-csv
  quicklook-json
  quicklookase
  webpquicklook
  rdm
  #recordit
  slack
  skype
  thunder
  virtualbox
  vagrant
  visual-studio-code
)

# Fonts
fonts=(
  font-source-code-pro
  font-source-code-pro-for-powerline
)

echo "Update Homebrew..."
# Update homebrew recipes
brew update

# Install GNU core utilities (those that come with OS X are outdated)
brew install coreutils
# Install GNU `find`, `locate`, `updatedb`, and `xargs`, g-prefixed
brew install findutils
# Install Bash 4
brew install bash
# Install Homebrew Cask
brew tap caskroom/fonts
brew tap caskroom/versions

brew tap eddieantonio/eddieantonio

echo "Installing binaries..."
brew install ${binaries[@]}

echo "Installing fonts..."
brew cask install ${fonts[@]}

# Install apps to /Applications
# Default is: /Users/$user/Applications
echo "Installing apps..."
sudo brew cask install -v --appdir="/Applications" ${apps[@]}

# clean things up
brew cleanup
brew cask cleanup

exit 0
