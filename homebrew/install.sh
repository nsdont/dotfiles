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
  autoconf
  autoenv
  autojump
  cmake
  coreutils
  curl
  ctags
  erlang
  fortune
  freetype
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
  fortune
  openjpeg
  macvim
  mackup
  mysql
  nginx
  nmap
  node
  openjpeg
  openssl
  postgresql
  python
  python3
  rabbitmq
  redis
  ssh-copy-id
  sqlite
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
  calibre
  dash
  dropbox
  dockertoolbox
  dayone-cli
  evernote
  flux
  google-chrome
  istat-menus
  iterm2
  kaleidoscope
  keka
  kindle
  mou
  mplayerx
  moom
  navicat-premium
  neteasemusic
  nutstore
  omnifocus
  omnigraffle
  omnioutliner
  omniplan
  paw
  qlcolorcode
  qlmarkdown
  qlstephen
  qq
  rdm
  recordit
  seafile-client
  shadowsocksx
  skype
  sourcetree
  sogouinput
  sublime-text3
  textexpander
  thunder
  today-scripts
  utorrent
  virtualbox
  vagrant
)

# Fonts
fonts=(
  font-source-code-pro
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
brew install caskroom/cask/brew-cask

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
