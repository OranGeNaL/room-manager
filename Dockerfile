FROM orangenal/roombot-env
# RUN pip install pytelegrambotapi
COPY . /app
#RUN pip install wakeonlan
#RUN apt-get install etherwake
#ENTRYPOINT [ "/bin/bash", "/app/start.sh" ]
ENTRYPOINT [ "python3", "/app/code/bot.py" ]