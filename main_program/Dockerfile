FROM ubuntu:latest
WORKDIR /
COPY ./docker/firefox.tar.bz2 ./docker/{a6c4a591-f1b2-4f03-b3ff-767e5bedf4e7}.xpi /opt/ 

COPY ./docker/mgba.appimage ./docker/pkmn_ultravhak.gba /game/
COPY ./docker/config.ini /
COPY ./app/pokemon_api.py ./app/requirements.txt ./app/.env /app/

ENV DISPLAY=:20
ENV USER=root
ENV DEBIAN_FRONTEND noninteractive
EXPOSE 8894:8894

RUN apt-get update && \
apt-get install apt-utils -f -y && \
apt-get install python3 python3-tk python3-dev -f -y && \
apt-get install pip -f -y && \
apt-get install x11vnc -f -y && \
apt-get install net-tools -f -y && \
apt-get install bzip2 -f -y && \
apt-get install libdbus-glib-1-2 -y && \
apt-get install openbox -f -y && \
apt-get install ssh -f -y && \
apt-get install openjdk-11-jre -f -y && \
apt-get install alsa-utils -f -y && \
apt-get install wmctrl -f -y && \ 
apt-get install p7zip-full -f -y && \
apt-get install libasound2 -f -y && \
apt-get install xinit -f -y && \
apt-get install libxkbcommon0 -f -y && \
apt-get install libxkbcommon-x11-0 -f -y && \
apt-get install xvfb -f -y && \
tar xjf /opt/firefox.tar.bz2 && \
mv /firefox /opt/ && \
ln -s /opt/firefox/firefox /bin/firefox && \
mkdir /opt/firefox/distribution && \
mkdir /opt/firefox/distribution/extensions && \
mv '/opt/{a6c4a591-f1b2-4f03-b3ff-767e5bedf4e7}.xpi' '/opt/firefox/distribution/extensions/' && \
mkdir ~/.vnc && \
touch ~/.vnc/passwd && \
DISPLAY=:20 && \
export DISPLAY && \
x11vnc -storepasswd "L3tme1n" ~/.vnc/passwd && \
echo "exec openbox-session &" > ~/.xinitrc && \
echo "exec xterm" >> ~/.xinitrc && \
echo "/usr/bin/x11vnc -forever -usepw -rfbport 8894 -create &" > /opt/start_script.sh && \
echo "echo 'Executed primary loop, connect to port 8894 to view screen; press enter to quit'" >> /opt/start_script.sh && \
echo "while [-z '$(xdpyinfo &>/dev/null)']; do echo 'awaiting proper xsession before starting game and python script'; sleep 1; done" >> /opt/start_script.sh && \
echo "sleep 5" >> /opt/start_script.sh && \
echo "/game/mgba.appimage --appimage-extract" >> /opt/start_script.sh && \
echo "mkdir ~/.config" >> /opt/start_script.sh && \
echo "mkdir ~/.config/mgba/" >> /opt/start_script.sh && \
echo "mv /config.ini ~/.config/mgba/" >> /opt/start_script.sh && \
echo "/squashfs-root/AppRun /game/pkmn_ultravhak.gba &" >> /opt/start_script.sh && \
echo "python3 /app/pokemon_api.py" >> /opt/start_script.sh && \
chmod +x /opt/start_script.sh

CMD "/opt/start_script.sh"