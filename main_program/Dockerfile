FROM ubuntu:latest
WORKDIR /

COPY ./docker/mgba.appimage ./docker/pkmn_ultravhak.gba /game/
COPY ./docker/config.ini /
COPY ./app/pokemon_api.py ./app/requirements.txt ./app/.env /app/
COPY ./docker/.Xauthority /root/

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
apt-get install tigervnc-viewer -f -y && \
apt-get install gnome-screenshot -f -y && \
apt-get install xvfb -f -y && \
mkdir ~/.vnc && \
touch ~/.vnc/passwd && \
DISPLAY=:20 && \
export DISPLAY && \
x11vnc -storepasswd "L3tme1n" ~/.vnc/passwd && \
echo "exec openbox-session &" > ~/.xinitrc && \
echo "exec xterm" >> ~/.xinitrc && \
echo "xvfb-run --server-args='-screen 0, 1024x768x16' vncviewer -passwd L3tme1n localhost::8894 & sleep 2; kill $!" > /opt/fake_vnc.sh && \
#echo "Xvfb $DISPLAY -screen 0 1024x768x16 &" >> /opt/start_script.sh && \
echo "/usr/bin/x11vnc -forever -usepw -rfbport 8894 -create &" > /opt/start_script.sh && \
echo "sleep 2" >> /opt/start_script.sh && \
echo "/opt/fake_vnc.sh" >> /opt/start_script.sh && \
echo "sleep 3" >> /opt/start_script.sh && \
echo "/game/mgba.appimage --appimage-extract" >> /opt/start_script.sh && \
echo "mkdir ~/.config" >> /opt/start_script.sh && \
echo "mkdir ~/.config/mgba/" >> /opt/start_script.sh && \
echo "mv /config.ini ~/.config/mgba/" >> /opt/start_script.sh && \
echo "/squashfs-root/AppRun /game/pkmn_ultravhak.gba &" >> /opt/start_script.sh && \
echo "pip install -r /app/requirements.txt" >> /opt/start_script.sh && \
echo "python3 /app/pokemon_api.py" >> /opt/start_script.sh && \
chmod +x /opt/fake_vnc.sh && \
chmod +x /opt/start_script.sh

CMD "/opt/start_script.sh"