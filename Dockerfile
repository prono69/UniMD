RUN curl -s https://raw.githubusercontent.com/yshalsager/megadown/master/megadown -o ./megadown && sudo chmod a+x ./
RUN curl -s https://raw.githubusercontent.com/yshalsager/cmrudl.py/master/cmrudl.py -o ./cmrudl && sudo chmod a+x ./
ENV PATH="./:$PATH"
