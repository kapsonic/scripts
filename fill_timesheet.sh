mkdir ~/tmp
source git_messages.sh $1 > ~/tmp/messages.git.log
java -jar ~/Scripts/selenium-server-standalone-2.51.0.jar
ruby ~/Scripts/nb.rb
