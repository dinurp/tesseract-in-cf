# tesseract-in-cf
- Deployent of tesseract in CF
- Sample Flask app using pytesseract

#how to create tesseract-ocr-mrz.deb?

~~~
mkdir -p tesseract-ocr-mrz/DEBIAN
cat - > tesseract-ocr-mrz/DEBIAN/control <<EOF
Package: tesseract-ocr-mrz
Source: tesseract-lang
Version: 4.00~git-0f039b
Architecture: all
Maintainer: Ubuntu Developers <ubuntu-devel-discuss@lists.ubuntu.com>
Recommends: tesseract-ocr (>= 3.99)
Breaks: tesseract-ocr (<< 3.99)
Replaces: tesseract-ocr-data (<< 2)
Provides: tesseract-ocr-lang, tesseract-ocr-language
Section: graphics
Priority: optional
Homepage: https://github.com/DoubangoTelecom/tesseractMRZ
Description: tesseract-ocr language files for Machine Readable Zone (MRZ)
 Tesseract is an open source Optical Character Recognition (OCR)
 Engine. It can be used directly, or (for programmers) using an API to
 extract printed text from images. This package contains the data
 needed for processing images of MRZ in ID documents..
EOF

mkdir -p tesseract-ocr-mrz/usr/share/tesseract-ocr/4.00/tessdata
wget  -O tesseract-ocr-mrz/usr/share/tesseract-ocr/4.00/tessdata/mrz.traineddata \
         https://github.com/DoubangoTelecom/tesseractMRZ/raw/master/tessdata_best/mrz.traineddata

find tesseract-ocr-mrz -type d | xargs chmod 755
sudo chown root:root -R tesseract-ocr-mrz
sudo dpkg-deb --build tesseract-ocr-mrz

~~~

upload tesseract-ocr-mrz.deb somewhere where .deb extension can be retained and refer to it from apt.yaml.

reference: 
- https://github.com/DoubangoTelecom/tesseractMRZ
- http://tldp.org/HOWTO/html_single/Debian-Binary-Package-Building-HOWTO/#AEN108 
- http://archive.ubuntu.com/ubuntu/pool/universe/t/tesseract-lang/tesseract-ocr-eng_4.00~git24-0e00fe6-1.2_all.deb 
