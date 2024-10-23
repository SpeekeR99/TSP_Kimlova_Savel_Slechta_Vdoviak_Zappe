# https://github.com/docker-library/python/blob/37a6827e0b7a9ef099cfdec5de305e3d4cea7331/3.9/slim-bookworm/Dockerfile
FROM python:3.9-slim 

WORKDIR /ai

# updates archive area
RUN echo "deb http://deb.debian.org/debian bookworm contrib non-free" > /etc/apt/sources.list.d/contrib.list
# install required packages
RUN apt-get clean && apt-get update \
&& apt-get install -y \
	ffmpeg \
	libsm6 libxext6 \
	# for fonts
	ttf-mscorefonts-installer fontconfig \
	# for QR code
	libzbar0 \
	# for wkhtmltopdf
	wget xvfb libfontconfig1 libxrender1

ENV ENV=production
ARG TARGETPLATFORM

# install wkhtmltopdf`
RUN case "$TARGETPLATFORM" in \
	"linux/amd64")	ARCH="amd64" ;; \
	"linux/arm64")	ARCH="arm64" ;; \
	*)				echo "Unsupported platform: $TARGETPLATFORM" && exit 1 ;; \
	esac && \
	wget -q -O wkhtmltox.deb https://github.com/wkhtmltopdf/packaging/releases/download/0.12.6.1-3/wkhtmltox_0.12.6.1-3.bookworm_${ARCH}.deb

# This will crash on:
# dpkg: dependency problems prevent configuration of wkhtmltox:
#	wkhtmltox depends on xfonts-75dpi; however:
#		Package xfonts-75dpi is not installed.
# So we have to fix deps on non-zero return call
# More here: https://askubuntu.com/questions/604029/dependency-problems-with-wkhtmltopdf-when-trying-to-install-latest-version
RUN dpkg -i wkhtmltox.deb || apt-get install -f -y

# refresh system font cache
RUN fc-cache -f -v

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV MONGO_DB_PORT=27017
ENV MONGO_DB_HOST=mongodb_service

EXPOSE 8081

CMD ["python", "src/api/api_gateway.py"]