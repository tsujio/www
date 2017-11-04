FROM httpd

RUN sed -i -e 's/#\(LoadModule negotiation_module modules\/mod_negotiation.so\)/\1/' \
    /usr/local/apache2/conf/httpd.conf

RUN sed -i -e 's/\(DirectoryIndex index.html\)/\1 index.html.var/' \
    /usr/local/apache2/conf/httpd.conf

RUN sed -i -e 's/#\(AddHandler type-map var\)/\1/' \
    /usr/local/apache2/conf/httpd.conf

RUN rm /usr/local/apache2/htdocs/index.html

COPY ./html /usr/local/apache2/htdocs
