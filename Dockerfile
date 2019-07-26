RUN curl -s https://raw.githubusercontent.com/yshalsager/megadown/master/megadown -o /home/userbot/bin/megadown && sudo chmod a+x /home/userbot/bin/megadown
RUN curl -s https://raw.githubusercontent.com/yshalsager/cmrudl.py/master/cmrudl.py -o /home/userbot/bin/cmrudl && sudo chmod a+x /home/userbot/bin/cmrudl
ENV PATH="/home/userbot/bin:$PATH"
