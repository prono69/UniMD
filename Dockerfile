RUN curl -s https://raw.githubusercontent.com/yshalsager/megadown/master/megadown -o /home/userbot/bin/megadown && sudo chmod a+x ./
RUN curl -s https://raw.githubusercontent.com/yshalsager/cmrudl.py/master/cmrudl.py -o /home/userbot/bin/cmrudl && sudo chmod a+x ./
ENV PATH="./:$PATH"
