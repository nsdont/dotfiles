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
  boot2docker
  autojump
  cmake
  coreutils
  curl
  ctags
  docker
  erlang
  freetype
  go
  git
  git-flow
  gettext
  goaccess
  graphviz
  htop-osx
  wget
  redis
  jpeg
  libxml++
  libffi
  libpng
  libtiff
  libyaml
  ruby
  fortune
  openjpeg
  macvim
  mackup
  mysql
  sqlite
  zsh-completions
  freetype
  postgresql
  goaccess
  python
  python3
  ssh-copy-id
  trash
  tree
)

# Apps
apps=(
  1password
  alfred
  calibre
  catchmouse
  dash
  dropbox
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
  navicat-premium
  neteasemusic
  nutstore
  obs
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
  shadowsocksx
  steam
  skype
  sourcetree
  sublime-text3
  textexpander
  thunder
  today-scripts
  utorrent
  virtualbox
)

# Fonts
fonts=(
  font-roboto
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

echo "Installing binaries..."
brew install ${binaries[@]}

echo "Installing fonts..."
brew cask install ${fonts[@]}

# Install apps to /Applications
# Default is: /Users/$user/Applications
echo "Installing apps..."
sudo brew cask install --appdir="/Applications" ${apps[@]}

# clean things up
brew cleanup
brew cask cleanup

exit 0
